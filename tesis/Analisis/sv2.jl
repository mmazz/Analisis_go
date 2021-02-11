include("../src/TrueSkill.jl")
using .TrueSkill
global const ttt = TrueSkill
using Test
using CSV
using DataFrames
using Random
using Distributions

iteration = 12
info = false
leng = 1000
@testset "Examples" begin
    # 0 gana, 1 pierde

    @testset "Best gamma" begin
        # no le habia agregado 25?
        function skill(alpha::Int64)
            return 1/(1+exp((-1*alpha + leng/2)/80)) + 25
        end

        mean_agent = [skill(i) for i in 1:leng]
        beta = 1.
        ev = -1000
        Random.seed!(1)

        mean_target = [(Random.randn(1)[1]*beta + skill(i)) for i in 1:1000]
        perf_target = [(Random.randn(1)[1]*beta + mean_target[i]) for i in 1:1000]
        perf_agent = [(Random.randn(1)[1]*beta + mean_target[i]) for i in 1:1000]
        events = [ [["a"], [string(i)] ] for i in 1:1000]
        results = [ perf_agent[i] > perf_target[i] ? [0,1] : [1,0] for i in 1:1000 ]
        batches= [i for i in 1:1000 ]

        #selected_gammas = [0.005,0.02,0.055,0.1,1]
        selected_gammas = [0.005,0.02,0.055,0.1,1]
        #gammas = [gamma for gamma in 0.001:0.001:0.04]
        gammas = [gamma for gamma in range(0.001,stop=0.01,length=14)]
        gammas[7] = 0.005
        println(gammas)
        gamma2 = [gamma for gamma in range(0.01,stop=0.1,length=13)]
        gamma2[3] = 0.02
        gamma2[4] = 0.0325
        println(gamma2)

        gamma3 = [gamma for gamma in range(0.1,stop=1,length=13)]
        gammas = cat(gammas,gamma2,dims =(1, 1))
        gammas = cat(gammas,gamma3,dims =(1, 1))
        evidencias_ts = Float64[]
        evidencias_ttt = Float64[]
        learning_curves = Vector{Vector{Float64}}()
        info && println(gammas)
        for gamma in gammas#gamma=0.02
            priors = Dict{String,ttt.Rating}()
            priors["a"] = ttt.Rating(25., 6.0, beta, gamma)
            for k in 1:1000
                priors[string(k)] = ttt.Rating(mean_target[k], 0.5, beta, 0.0)
            end
            h = ttt.History(events, results, batches, priors, ttt.Environment(iter=iteration))
            push!(evidencias_ts, ttt.log_evidence(h))
            ttt.convergence(h, info)

            push!(evidencias_ttt, ttt.log_evidence(h))
            if gamma in selected_gammas
                info && println(gamma)
                push!(learning_curves, [r.mu for (t, r) in ttt.learning_curves(h)["a"]] )
            end
        end
        println(gammas[argmax(evidencias_ttt)])
        @test 0.02 == gammas[argmax(evidencias_ttt)]
        df = DataFrame(gammas = gammas
                        ,evidencias_ts = evidencias_ts/ev
                        ,evidencias_ttt = evidencias_ttt/ev)
        CSV.write("../Presentacion/SV_ev2.csv", df; header=true)
        println("lc")
        # [0.005,0.02,0.055,0.1,1]
        df = DataFrame(mean_agent = mean_agent
                        ,lc_0005 = learning_curves[1]
                        ,lc_002  = learning_curves[2]
                        ,lc_0055 = learning_curves[3]
                        ,lc_01 = learning_curves[4]
                        ,lc_1 = learning_curves[5])
        CSV.write("../Presentacion/SV2.csv", df; header=true)
    end

end
