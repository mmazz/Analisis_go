include("./src/TrueSkill.jl")
using .TrueSkill
global const ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames
using LinearAlgebra

data = CSV.read("./simulacion.csv")

results = [row.player2_win == 1 ? [1, 0] : [0, 1] for row in eachrow(data) ]
composition = [[[string(r.jugador1)],[string(r.jugador2)]]  for r in eachrow(data) ]
beta = 25/6
gammas = [0.25,30.0]


matrix_ev = zeros(Float64, length(gammas)) # filas columnas

ttt.setbeta(beta)

for j in 1:length(gammas)
    h = 0
    evidence=0
    times = Vector{Int64}()
    ttt.setgamma(gammas[j])

    h = ttt.History(composition, results, times )
    ttt.convergence(h)

    evidence = [ h.batches[r].evidences[1] for r in 1:size(data)[1]]
    logevidence = -1*log.(evidence)
    prom_log_ev = sum(logevidence)/length(evidence)
    println(prom_log_ev)
    matrix_ev[j] = prom_log_ev
end


println(matrix_ev)
#df = DataFrame(matrix_ev)
#DataFrames.rename!(df, [Symbol("Gamma=$i") for i in gammas])
#insert!(df, 1, gammas, :gammas)
#CSV.write("matrix_ev_gammas.csv",  df, writeheader=true)
