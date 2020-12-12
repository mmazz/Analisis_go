include("../src/TrueSkill.jl")
using .TrueSkill
global const ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames
data = CSV.read("../img/KGS_filtered.csv")
#data = CSV.read("../img/KGS_filtered_NoKomi.csv")
leng = 500000
info = false
iteracion = 6
# Pruebo hacer el estudio de rela de sigma beta sin handicap. Y useo ese criterio
# para despues usarlo con.
# ver si cambia algo

################################################################################
######################## Barrido TS BETA/SIGMA #################################
################################################################################
# #=
data = CSV.read("../img/KGS_filtered.csv")
data_small = data[1:leng,:]


evidencias_ts = Float64[]
evidencias_ttt = Float64[]
fracs = [3.0,6.0,9.0]
global evidencias_ttt = Vector{Vector{Float64}}()
for i in 1:1:length(fracs)
     push!(evidencias_ttt, [])
end

for j in 1:1:length(fracs)
    println(" ")
    println(fracs[j])

    global gammas = [gamma for gamma in range(0.0001,stop=0.025,length=15)]
    beta_h = 1.0
    sigma_h = fracs[j]*beta_h
    #evidencias_ts = Float64[]
    learning_curves = Vector{Vector{Float64}}()
    for gamma in gammas#gamma=0.015
        priors = Dict{String,ttt.Rating}()
        for h_key in Set([(row.handicap, row.width) for row in eachrow(data_small) ])
            priors[string(h_key)] = ttt.Rating(25.,sigma_h,0.0,0.0)
        end
        results = [row.black_win == 1 ? [1,0] : [0, 1] for row in eachrow(data_small) ]
        #events = [ r.handicap<2 ? [[string(r.white)],[string(r.black)]] : [[string(r.white)],[string(r.black)]] for r in eachrow(data_small) ]
        events = [[[string(r.white)],[string(r.black),string(r.handicap)]] for r in eachrow(data_small) ]
        #batches = [row.date for row in eachrow(data)]
        batches = Vector{Int64}()
        env = ttt.Environment(mu=25., sigma=sigma_h, beta=beta_h, gamma=gamma,p_draw=0.0, epsilon=1e-6,iter=iteracion)
        h = ttt.History(events, results, batches, priors, env)
        push!(evidencias_ts, ttt.log_evidence(h))
        println("Gamma: ",gamma, " evidencia ts: ",ttt.log_evidence(h))
        #ttt.convergence(h)
        push!(evidencias_ttt[j], ttt.log_evidence(h))
        #println( " ttt: ", ttt.log_evidence(h))

    end
    println("Mejor Gamma", gammas[argmax(evidencias_ttt)])
end
df = DataFrame(gammas = gammas
              ,tres_beta = evidencias_ttt[1]
              ,seis_beta = evidencias_ttt[2]
              ,nueve_beta = evidencias_ttt[3]
              )

CSV.write("../img/Datos/rela_beta_sigma_gamma0.csv", df; header=true)
#CSV.write("./ConKomi/rela_beta_sigma.csv", df; header=true)
# =#
################################################################################
######################## Barrido TTT BETA/SIGMA #################################
################################################################################
## =
# Con todos los handicaps
data = CSV.read("../img/KGS_filtered.csv")
data_small = data[1:leng,:]

global gammas = [gamma for gamma in range(0.0025,stop=0.025,length=10)]
beta_h = 1.0
sigma_h = 3.0*beta_h
evidencias_ts = Float64[]
evidencias_ttt = Float64[]
learning_curves = Vector{Vector{Float64}}()

for gamma in gammas
    priors = Dict{String,ttt.Rating}()
    for h_key in Set([(row.handicap, row.width) for row in eachrow(data_small) ])
        priors[string(h_key)] = ttt.Rating(25., sigma_h, 0.0, 0.0)
    end
    results = [row.black_win == 1 ? [1,0] : [0, 1] for row in eachrow(data_small) ]
    events = [ [[string(r.white)],[string(r.black),string(r.handicap)]] for r in eachrow(data_small) ]
    batches = Vector{Int64}()
    env = ttt.Environment(mu=25., sigma=sigma_h, beta=beta_h, gamma=gamma,p_draw=0.0, epsilon=1e-6,iter=iteracion)
    h = ttt.History(events, results, batches, priors, env)
    push!(evidencias_ts, ttt.log_evidence(h))
    info && println("Gamma: ",gamma, " evidencia ts: ",ttt.log_evidence(h))
    ttt.convergence(h, info)
    push!(evidencias_ttt, ttt.log_evidence(h))
    info && println( " ttt: ", ttt.log_evidence(h))
end
info && println("Mejor Gamma", gammas[argmax(evidencias_ttt)])



df = DataFrame(gammas = gammas
          ,tres_beta_ts = evidencias_ts
          ,tres_beta_ttt = evidencias_ttt
          )

CSV.write("../img/Datos/rela_beta_sigma_zoom_gamma0.csv", df; header=true)


#=

# Sin considerar handicap
data = CSV.read("../img/KGS_filtered.csv")
data_small = data[1:leng,:]

global gammas = [gamma for gamma in range(0.002,stop=0.05,length=10)]
beta_h = 1.0
sigma_h = 3.0*beta_h
evidencias_ts = Float64[]
evidencias_ttt = Float64[]
learning_curves = Vector{Vector{Float64}}()

for gamma in gammas
    priors = Dict{String,ttt.Rating}()
    results = [row.black_win == 1 ? [1,0] : [0, 1] for row in eachrow(data_small) ]
    events = [[[string(r.white)],[string(r.black)]] for r in eachrow(data_small) ]
    batches = Vector{Int64}()
    env = ttt.Environment(mu=25., sigma=sigma_h, beta=beta_h, gamma=gamma,p_draw=0.0, epsilon=1e-6,iter=iteracion)
    h = ttt.History(events, results, batches, priors, env)
    push!(evidencias_ts, ttt.log_evidence(h))
    info && println("Gamma: ",gamma, " evidencia ts: ",ttt.log_evidence(h))
    ttt.convergence(h, info)
    push!(evidencias_ttt, ttt.log_evidence(h))
    info && println( " ttt: ", ttt.log_evidence(h))
end
info && println("Mejor Gamma", gammas[argmax(evidencias_ttt)])



df = DataFrame(gammas = gammas
          ,tres_beta_ts = evidencias_ts
          ,tres_beta_ttt = evidencias_ttt
          )

CSV.write("../img/Datos/rela_beta_sigma_zoom_noH.csv", df; header=true)


 =#















#=
# Con handicap pero sin H1
data = CSV.read("../img/KGS_filtered.csv")
data_small = data[1:leng,:]

global gammas = [gamma for gamma in range(0.002,stop=0.012,length=10)]
beta_h = 1.0
sigma_h = 3.0*beta_h
evidencias_ts = Float64[]
evidencias_ttt = Float64[]
learning_curves = Vector{Vector{Float64}}()

for gamma in gammas
    priors = Dict{String,ttt.Rating}()
    for h_key in Set([(row.handicap, row.width) for row in eachrow(data_small) ])
        priors[string(h_key)] = ttt.Rating(25., sigma_h, 0.0, gamma)
    end
    results = [row.black_win == 1 ? [1,0] : [0, 1] for row in eachrow(data_small) ]
    events = [ r.handicap<2 ? [[string(r.white)],[string(r.black)]] : [[string(r.white)],[string(r.black),string(r.handicap)]] for r in eachrow(data_small) ]
    batches = Vector{Int64}()
    env = ttt.Environment(mu=25., sigma=sigma_h, beta=beta_h, gamma=gamma,p_draw=0.0, epsilon=1e-6,iter=iteracion)
    h = ttt.History(events, results, batches, priors, env)
    push!(evidencias_ts, ttt.log_evidence(h))
    info && println("Gamma: ",gamma, " evidencia ts: ",ttt.log_evidence(h))
    ttt.convergence(h, info)
    push!(evidencias_ttt, ttt.log_evidence(h))
    info && println( " ttt: ", ttt.log_evidence(h))
    info && println( " ttt: ", ttt.log_evidence(h))
end
info && println("Mejor Gamma", gammas[argmax(evidencias_ttt)])



df = DataFrame(gammas = gammas
          ,tres_beta_ts = evidencias_ts
          ,tres_beta_ttt = evidencias_ttt
          )

CSV.write("../img/Datos/rela_beta_sigma_zoom_noH1.csv", df; header=true)
#CSV.write("./ConKomi/TS_rela_beta_sigma_zoom.csv", df; header=true)
=#
################################################################################
######################## Barrido TTT BETA/SIGMA #################################
################################################################################
# =#
#=
leng = 800000
data_small = data[1:leng,:]
data_small = data
iteracion = 10
global gammas = [gamma for gamma in range(0.008,stop=0.02,length=5)]
beta_h = 1.0
sigma_h = 3.0*beta_h
evidencias_ts = Float64[]
evidencias_ttt = Float64[]
learning_curves = Vector{Vector{Float64}}()

for gamma in gammas
    priors = Dict{String,ttt.Rating}()
    for h_key in Set([(row.handicap, row.width) for row in eachrow(data_small) ])
        priors[string(h_key)] = ttt.Rating(25.,sigma_h,0.0,gamma)
    end
    results = [row.black_win == 1 ? [1,0] : [0, 1] for row in eachrow(data_small) ]
    #events = [ [[string(r.white)],[string(r.black)]] for r in eachrow(data_small) ]
    events = [ r.handicap<2 ? [[string(r.white)],[string(r.black)]] : [[string(r.white)],[string(r.black),string(r.handicap)]] for r in eachrow(data_small) ]
    #events = [[[string(r.white)],[string(r.black),string(r.handicap)]]   for r in eachrow(data_small) ]
    #batches = [row.date for row in eachrow(data)]
    batches = Vector{Int64}()
    env = ttt.Environment(mu=25., sigma=sigma_h, beta=beta_h, gamma=gamma,p_draw=0.0, epsilon=1e-6,iter=iteracion)
    h = ttt.History(events, results, batches, priors, env)
    push!(evidencias_ts, ttt.log_evidence(h))
    println("Gamma: ",gamma, " evidencia ts: ",ttt.log_evidence(h))
    ttt.convergence(h)
    push!(evidencias_ttt, ttt.log_evidence(h))
    println( " ttt: ", ttt.log_evidence(h))
end
println("Mejor Gamma", gammas[argmax(evidencias_ttt)])



df = DataFrame(gammas = gammas
          ,tres_beta_ts = evidencias_ts
          ,tres_beta_ttt = evidencias_ttt
          )

CSV.write("../img/Datos/rela_beta_sigma_zoom_H_no1.csv", df; header=true)
=#
