include("../src/TrueSkill.jl")
using .TrueSkill
global const ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames
data = CSV.read("../img/Datos/TrainSet_sameRank.csv")

evidencias_ts = Float64[]
evidencias_ttt = Float64[]
beta_h =  1.0/(0.21844648724*1.011657753913105*1.0162)
sigma_h = 3.0*beta_h
gamma = 0.0075
iteracion = 12

prior_dict = Dict{String,ttt.Rating}()
for h_key in Set([row.handicap for row in eachrow(data) ])
    prior_dict[string(h_key)] = ttt.Rating(25.,sigma_h,0., 0.0)
end
results = [row.black_win == 1 ? [1,0] : [0, 1] for row in eachrow(data)]
events = [ [[string(r.white)],[string(r.black),string(r.handicap)]] for r in eachrow(data) ]
batches = Vector{Int64}()

env = ttt.Environment(mu=25.0, sigma=sigma_h, beta=beta_h, gamma=gamma, p_draw=0.0, epsilon=1e-6,iter=iteracion)
h = ttt.History(events, results, batches , prior_dict, env)

#println("Purifing Data TS")

#w_mean = [ ttt.posterior(h.batches[r], string(data[r,"white"])).mu for r in 1:size(data)[1]]
#b_mean = [ ttt.posterior(h.batches[r], string(data[r,"black"])).mu  for r in 1:size(data)[1]]
#w_std = [ ttt.posterior(h.batches[r], string(data[r,"white"])).sigma for r in 1:size(data)[1]]
#b_std = [ ttt.posterior(h.batches[r], string(data[r,"black"])).sigma for r in 1:size(data)[1]]
push!(evidencias_ts, ttt.log_evidence(h))
#w_mean_prior = [ ttt.within_priors(h.batches[r], 1)[1][1].N.mu for r in 1:size(data)[1]]
#b_mean_prior = [ ttt.within_priors(h.batches[r], 1)[2][1].N.mu for r in 1:size(data)[1]]
#w_std_prior = [ ttt.within_priors(h.batches[r], 1)[1][1].N.sigma for r in 1:size(data)[1]]
#b_std_prior = [ ttt.within_priors(h.batches[r], 1)[2][1].N.sigma for r in 1:size(data)[1]]

#println("Saving Data TS")
#df = DataFrame(id = data[:"id"]
#              ,white = data[:"white"]
#              ,black = data[:"black"]
#              ,started = data[:"started"]
#              ,w_mean = w_mean
#              ,b_mean = b_mean
#              ,w_std = w_std
#              ,b_std = b_std
#              ,w_mean_prior = w_mean_prior
#              ,b_mean_prior = b_mean_prior
#              ,w_std_prior = w_std_prior
#              ,b_std_prior = b_std_prior
#              )
#
#CSV.write("../img/Datos/TrainingSet_diffRank_TS.csv", df; header=true)

println("Starting TTT")
ttt.convergence(h)

println("Purifing Data TTT")
w_mean = [ ttt.posterior(h.batches[r], string(data[r,"white"])).mu for r in 1:size(data)[1]]
b_mean = [ ttt.posterior(h.batches[r], string(data[r,"black"])).mu  for r in 1:size(data)[1]]
w_std = [ ttt.posterior(h.batches[r], string(data[r,"white"])).sigma for r in 1:size(data)[1]]
b_std = [ ttt.posterior(h.batches[r], string(data[r,"black"])).sigma for r in 1:size(data)[1]]
push!(evidencias_ttt, ttt.log_evidence(h))

println("Saving Data TTT")
#id = data[:"id"],
df = DataFrame(white = data[:"white"]
              ,black = data[:"black"]
              #,handicap = data[:"handicap"]
              #,width = data[:"width"]
              #,whiteRank = data[:"whiteRank"]
              #,blackRank = data[:"blackRank"]
              #,komi = data[:"komi"]
              #,started = data[:"started"]
              ,black_win = data[:"black_win"]
              ,w_mean = w_mean
              ,b_mean = b_mean
              ,w_std = w_std
              ,b_std = b_std
              )


CSV.write("../img/Datos/TrainingSet_sameRank_TTT.csv", df; header=true)
df = DataFrame(evidencias_ts = evidencias_ts
                ,evidencias_ttt = evidencias_ttt)
CSV.write("../img/Datos/TrainingSet_sameRank_evidence.csv", df; header=true)
