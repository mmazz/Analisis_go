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
info = false
################################################################################
########################### PENDIENTE Handicap #################################
################################################################################
# sacando los bots el gamma sigue siendo igual!

## =
evidencias_ts = Float64[]
evidencias_ttt = Float64[]

beta_h = 1.0
sigma_h = 3.0*beta_h
gamma = 0.0075
iteracion = 6

prior_dict = Dict{String,ttt.Rating}()
for h_key in Set([(row.handicap, row.width) for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Rating(0.,sigma_h,0., 0.0)
end
results = [row.black_win == 1 ? [1,0] : [0, 1] for row in eachrow(data) ]
#events = [ r.handicap<2 ? [[string(r.white)],[string(r.black)]] : [[string(r.white)],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]
events = [[[string(r.white)],[string(r.black),string((r.handicap,r.width))]] for r in eachrow(data) ]

batches = Vector{Int64}()
env = ttt.Environment(mu=25.0, sigma=sigma_h, beta=beta_h, gamma=gamma, p_draw=0.0, epsilon=1e-6,iter=iteracion)
h = ttt.History(events, results, batches , prior_dict, env)
push!(evidencias_ts, ttt.log_evidence(h))

println("Starting TTT")
ttt.convergence(h, info)

println("Purifing Data TTT")
h_mean = [ data[r,"handicap"] >= 1 ? ttt.posterior(h.batches[r] ,string((data[r,"handicap"],data[r,"width"]))).mu : 0.0 for r in 1:size(data)[1]]
h_std = [ data[r,"handicap"] >= 1 ? ttt.posterior(h.batches[r] ,string((data[r,"handicap"],data[r,"width"]))).sigma : 0.0 for r in 1:size(data)[1]]
push!(evidencias_ttt, ttt.log_evidence(h))

println("Saving Data TTT")
df = DataFrame(handicap = data[:"handicap"]
              ,h_mean = h_mean
              ,h_std = h_std
              )

CSV.write("../img/Datos/TTT_H.csv", df; header=true)
df = DataFrame(evidencias_ts = evidencias_ts
                ,evidencias_ttt = evidencias_ttt)
CSV.write("../img/Datos/TTT_evidences_H.csv", df; header=true)
#
