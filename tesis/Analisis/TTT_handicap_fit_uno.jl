include("../src/TrueSkill.jl")
using .TrueSkill
global const ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames
data = CSV.read("../img/KGS_filtered.csv")

## =

evidencias_ts = Float64[]
evidencias_ttt = Float64[]

beta_h = 1.0/(0.21844648724*1.011657753913105*1.0162)  # .184/(0.6328*1.021)  #1.0/(0.3456*1.075359198570216) # = 3.184

sigma_h = 3.0*beta_h
gamma = 0.0075 # con H #gamma = 0.02 # no H
iteracion = 100

prior_dict = Dict{String,ttt.Rating}()

for h_key in Set([row.handicap for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Rating(25.,sigma_h,0., 0.)
end

results = [row.black_win == 1 ? [1,0] : [0, 1] for row in eachrow(data) ]
events = [[[string(r.white)],[string(r.black),string(r.handicap)]] for r in eachrow(data) ]
batches = Vector{Int64}()

env = ttt.Environment(mu=25.0, sigma=sigma_h, beta=beta_h, gamma=gamma, p_draw=0.0, epsilon=1e-6,iter=iteracion)
h = ttt.History(events, results, batches , prior_dict, env)
push!(evidencias_ts, ttt.log_evidence(h))
w_std_ts = [ ttt.posterior(h.batches[r], string(data[r,"white"])).sigma for r in 1:size(data)[1]]
b_std_ts = [ ttt.posterior(h.batches[r], string(data[r,"black"])).sigma for r in 1:size(data)[1]]

println("Starting TTT")
ttt.convergence(h)

println("Purifing Data TTT")
w_mean = [ttt.posterior(h.batches[r], string(data[r,"white"])).mu for r in 1:size(data)[1]]
b_mean = [ttt.posterior(h.batches[r], string(data[r,"black"])).mu  for r in 1:size(data)[1]]
w_std = [ ttt.posterior(h.batches[r], string(data[r,"white"])).sigma for r in 1:size(data)[1]]
b_std = [ ttt.posterior(h.batches[r], string(data[r,"black"])).sigma for r in 1:size(data)[1]]
h_mean = [ttt.posterior(h.batches[r] ,string(data[r,"handicap"])).mu for r in 1:size(data)[1]]
h_std = [ttt.posterior(h.batches[r] ,string(data[r,"handicap"])).sigma for r in 1:size(data)[1]]
push!(evidencias_ttt, ttt.log_evidence(h))
w_mean_prior = [ttt.within_priors(h.batches[r], 1)[1][1].N.mu for r in 1:size(data)[1]]
b_mean_prior = [ttt.within_priors(h.batches[r], 1)[2][1].N.mu for r in 1:size(data)[1]]
w_std_prior = [ttt.within_priors(h.batches[r], 1)[1][1].N.sigma for r in 1:size(data)[1]]
b_std_prior = [ttt.within_priors(h.batches[r], 1)[2][1].N.sigma for r in 1:size(data)[1]]
evindece = ttt.evidence(h)
println("Saving Data TTT")
df = DataFrame(id = data[:"id"]
              #,started = data[:"started"]
              ,white = data[:"white"]
              ,black = data[:"black"]
              ,handicap = data[:"handicap"]
              ,whiteRank = data[:"whiteRank"]
              ,blackRank = data[:"blackRank"]
              ,komi = data[:"komi"]
              ,black_win = data[:"black_win"]
              ,h_mean = h_mean
              ,h_std = h_std
              #,k_mean = k_mean
              #,k_std = k_std
              ,w_mean = w_mean
              ,b_mean = b_mean
              ,w_std = w_std
              ,b_std = b_std
              ,w_std_ts = w_std_ts
              ,b_std_ts = b_std_ts
              ,w_mean_prior = w_mean_prior
              ,b_mean_prior = b_mean_prior
              ,w_std_prior = w_std_prior
              ,b_std_prior = b_std_prior
              ,evidence = evindece
              )


CSV.write("../img/TTT_H_uno.csv", df; header=true)
df = DataFrame(evidencias_ts = evidencias_ts
                ,evidencias_ttt = evidencias_ttt)
CSV.write("../img/Datos/TTT_evidences_H_uno.csv", df; header=true)
# =#
