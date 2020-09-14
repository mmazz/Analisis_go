include("../../../paquetes/trueskill.jl/src/TrueSkill.jl")

using .TrueSkill
global const ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames
using Random

#Ver cuatro jugadores en los cuales se llevan 3 betas cada uno, la idea es Ver
#que a pesar de tener 100% de quien es el ganador, TS y TTT llegan a un estado
#de seguridad en el cual no actualiza mas y genera que el sigma deje de decrecer
#y de esa forma solo se agrega el gamma a la incertidumbre, es decir cada vez crece
#mas el sigma de cada jugador.
LENG = 1000
MU = 25.0
SIGMA = MU/3.0
BETA = MU/6.0
GAMMA = 0.0
function rendimiento(x,mu,sigma)
    y = (1/(sigma*(sqrt(2*pi))))*exp(-0.5*((x-mu)/sigma)^2)
    return y
end

x = range(MU-4*BETA,stop=MU+4*BETA,length=LENG)
y = rendimiento.(x,MU,BETA)



actualizacion_num_partidas = 50
valor_actualizacion = BETA/6
numero_partidas = 5000
Jugadores = Dict{String, Array{Float32,1}}("pepe" => [MU, 0], "juan" => [MU+3*BETA, 0], "ruben" => [MU+6*BETA, 0], "lol" => [MU+9*BETA, 0])
Jugadores_ev = Dict{String, Array{Float32,1}}
Jugador_estudio = "pepe"
jugador1 =  []
jugador2 =  []
player2_win = []
jugador1_real_skill = []
jugador2_real_skill = []

Random.seed!(1)
for i in 1:1:numero_partidas
    Jugadores_key = collect(keys(Jugadores))
    player1_key = Jugadores_key[rand(1:length(Jugadores_key))]
    player1 = Jugadores[player1_key]
    Jugadores_pop = copy(Jugadores)
    pop!(Jugadores_pop, player1_key)
    Jugadores_key_pop = collect(keys(Jugadores))
    player2_key = Jugadores_key_pop[rand(1:length(Jugadores_key_pop))]
    player2 = Jugadores[player2_key]
    player1_rend = Random.randn(1).*BETA.+player1[1]
    player2_rend = Random.randn(1).*BETA.+player2[1]
    diff = player1_rend - player2_rend
    if diff[1] > 0.0
        diff[1] = 1 # 1 de que perdio negro
    else
        diff[1] = 0
    end
    # flag conteo de partida de cada jugador
    Jugadores[player1_key][2] += 1
    Jugadores[player2_key][2] += 1
    if Jugadores[Jugador_estudio][2] >= actualizacion_num_partidas
        Jugadores[Jugador_estudio][1] += valor_actualizacion
        Jugadores[Jugador_estudio][2] = 0
    end
    push!(jugador1,player1_key)
    push!(jugador1_real_skill,Jugadores[player1_key][1])
    push!(jugador2,player2_key)
    push!(jugador2_real_skill,Jugadores[player2_key][1])
    #push!(resultados,diff)
    push!(player2_win,Int64(diff[1]))
end
data = Dict{Any, Any}("white"=> jugador1, "black"=> jugador2, "white_skill"=> jugador1_real_skill,
        "black_skill"=> jugador2_real_skill, "black_win"=> player2_win)
df = DataFrame(data)
CSV.write("./simulacion_crecimiento.csv", df; header=true)




data = DataFrame!(CSV.File("./simulacion_crecimiento.csv"))


prior_dict = Dict{String,ttt.Rating}()
#for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
#    prior_dict[string(h_key)] = ttt.Rating(0.,25.0/3.,0.,1.0/100)
#end
for key in Set([(row.white) for row in eachrow(data)])
    prior_dict[string(key)] = ttt.Rating(0.0,SIGMA,BETA,GAMMA)
end

results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(data) ]
composition = [[[string(r.white)],[string(r.black)]]  for r in eachrow(data) ]
times = Vector{Int64}()
#times = [row.date for row in eachrow(data)]


#println("Starting TrueSkill")
env=ttt.Environment(gamma=GAMMA,iter=20)
h = ttt.History(composition, results, times, prior_dict, env)
w_mean = [ ttt.posterior(h.batches[r], string(data[r,"white"])).mu for r in 1:size(data)[1]]
b_mean = [ ttt.posterior(h.batches[r], string(data[r,"black"])).mu  for r in 1:size(data)[1]]
w_std = [ ttt.posterior(h.batches[r], string(data[r,"white"])).sigma for r in 1:size(data)[1]]
b_std = [ ttt.posterior(h.batches[r], string(data[r,"black"])).sigma for r in 1:size(data)[1]]
evidence = [ h.batches[r].evidences[1] for r in 1:size(data)[1]]

println("Saving Data")
df = DataFrame(white = data[!,:"white"]
              ,black = data[!,:"black"]
              ,w_mean = w_mean
              ,b_mean = b_mean
              ,w_std = w_std
              ,b_std = b_std
              ,evidence = evidence)

#CSV.write("TTT_datos.csv", df; header=true)
CSV.write("Trueskill_datos_sin_handicap.csv", df; header=true)

println("Starting TTT")
ttt.convergence(h)

println("Purifing Data")
w_mean = [ ttt.posterior(h.batches[r], string(data[r,"white"])).mu for r in 1:size(data)[1]]
b_mean = [ ttt.posterior(h.batches[r], string(data[r,"black"])).mu  for r in 1:size(data)[1]]
w_std = [ ttt.posterior(h.batches[r], string(data[r,"white"])).sigma for r in 1:size(data)[1]]
b_std = [ ttt.posterior(h.batches[r], string(data[r,"black"])).sigma for r in 1:size(data)[1]]
evidence = [ h.batches[r].evidences[1] for r in 1:size(data)[1]]

println("Saving Data")
df = DataFrame(white = data[!,"white"]
              ,black = data[!,"black"]
              ,white_skill = data[!,"white_skill"]
              ,black_skill = data[!,"black_skill"]
              ,w_mean = w_mean
              ,b_mean = b_mean
              ,w_std = w_std
              ,b_std = b_std
              ,evidence = evidence)

#CSV.write("TTT_datos.csv", df; header=true)
CSV.write("TTT_datos_sin_handicap.csv", df; header=true)
