include("../../../paquetes/trueskill.jl/src/TrueSkill.jl")

using .TrueSkill
global const ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames
data = DataFrame!(CSV.File("./simulacion.csv"))
#data = data[1:300000,:]

#prior_dict = Dict{String,ttt.Rating}()
#for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
#    prior_dict[string(h_key)] = ttt.Rating(0.,25.0/3.,0.,1.0/100)
#end
results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(data) ]
composition = [[[string(r.white)],[string(r.black)]]  for r in eachrow(data) ]
times = Vector{Int64}()
#times = [row.date for row in eachrow(data)]

#println("Starting TrueSkill")
h = ttt.History(composition, results, times )
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
