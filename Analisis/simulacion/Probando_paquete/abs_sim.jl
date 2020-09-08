include("../../../paquetes/trueskill.jl/src/TrueSkill.jl")

using .TrueSkill
global const ttt = TrueSkill
using Test
using CSV
using JLD2
using Dates
using DataFrames
composition = [ [["aj"],["bj"]],[["bj"],["cj"]], [["cj"],["aj"]] ]
results = [[0,1],[0,1],[0,1]] 
bache = [1,2,3]
h = ttt.History(composition,results, bache)
println(ttt.posterior(h.batches[1],"aj"))
println(ttt.posterior(h.batches[1],"bj"))
ttt.convergence(h)

println(ttt.posterior(h.batches[1],"aj"))
println(ttt.posterior(h.batches[1],"bj"))
#println(ttt.posterior(h.batches[1],"cj"))
