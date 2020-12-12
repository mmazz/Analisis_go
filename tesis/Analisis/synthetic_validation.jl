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
@testset "Examples" begin
    # 0 gana, 1 pierde
    @testset "abc" begin
        events = [ [["aj"],["bj"]],[["bj"],["cj"]], [["cj"],["aj"]]]
        results = [[0,1],[0,1],[0,1]]
        priors = Dict{String,ttt.Rating}()
        for k in ["aj", "bj", "cj"]
            priors[k] = ttt.Rating(25., 6., 1., 0.0)
        end
        h = ttt.History(events, results, [1,2,3], priors, ttt.Environment(iter=iteration))
        lc_ts = ttt.learning_curves(h)
        ttt.convergence(h, info)
        lc_ttt = ttt.learning_curves(h)

        df = DataFrame(mu_a_ts = [ N.mu for (k,N) in lc_ts["aj"]]
                        ,sigma_a_ts = [ N.sigma for (k,N) in lc_ts["aj"]]
                        ,mu_a_ttt = [ N.mu for (k,N) in lc_ttt["aj"]]
                        ,sigma_a_ttt = [ N.sigma for (k,N) in  lc_ttt["aj"]]
                        ,time_a = [ k for (k,N) in lc_ts["aj"]]
                        ,mu_b_ts = [ N.mu for (k,N) in lc_ts["bj"]]
                        ,sigma_b_ts = [ N.sigma for (k,N) in lc_ts["bj"]]
                        ,mu_b_ttt = [ N.mu for (k,N) in lc_ttt["bj"]]
                        ,sigma_b_ttt = [ N.sigma for (k,N) in lc_ttt["bj"]]
                        ,time_b = [ k for (k,N) in lc_ts["bj"]]
                        ,mu_c_ts = [ N.mu for (k,N) in lc_ts["cj"]]
                        ,sigma_c_ts = [ N.sigma for (k,N) in lc_ts["cj"]]
                        ,mu_c_ttt = [ N.mu for (k,N) in lc_ttt["cj"]]
                        ,sigma_c_ttt = [ N.sigma for (k,N) in lc_ttt["cj"]]
                        ,time_c = [ k for (k,N) in lc_ts["cj"]]
                        )
        info && println("A: ",lc_ts["aj"]," B: ", lc_ts["bj"], " C: ",lc_ts["cj"])

        CSV.write("../img/Datos/SV_abc.csv", df; header=true)
        @test true
    end

    @testset "same_strength" begin
        events = [ [["aj"],["bj"]],[["bj"],["cj"]], [["cj"],["aj"]] ,
                    [["aj"],["bj"]],[["bj"],["cj"]], [["cj"],["aj"]],
                    [["aj"],["bj"]],[["bj"],["cj"]], [["cj"],["aj"]]]
        results = [[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]]
        priors = Dict{String,ttt.Rating}()
        for k in ["aj", "bj", "cj"]
            priors[k] = ttt.Rating(25., 6., 1.,0.)
        end
        h = ttt.History(events, results, [1,2,3,4,5,6,7,8,9], priors, ttt.Environment(iter=iteration))
        lc_ts = ttt.learning_curves(h)
        ttt.convergence(h, info)
        lc_ttt = ttt.learning_curves(h)

        df = DataFrame(mu_a_ts = [ N.mu for (k,N) in lc_ts["aj"]]
                        ,sigma_a_ts = [ N.sigma for (k,N) in lc_ts["aj"]]
                        ,mu_a_ttt = [ N.mu for (k,N) in lc_ttt["aj"]]
                        ,sigma_a_ttt = [ N.sigma for (k,N) in  lc_ttt["aj"]]
                        ,time_a = [ k for (k,N) in lc_ts["aj"]]
                        ,mu_b_ts = [ N.mu for (k,N) in lc_ts["bj"]]
                        ,sigma_b_ts = [ N.sigma for (k,N) in lc_ts["bj"]]
                        ,mu_b_ttt = [ N.mu for (k,N) in lc_ttt["bj"]]
                        ,sigma_b_ttt = [ N.sigma for (k,N) in lc_ttt["bj"]]
                        ,time_b = [ k for (k,N) in lc_ts["bj"]]
                        ,mu_c_ts = [ N.mu for (k,N) in lc_ts["cj"]]
                        ,sigma_c_ts = [ N.sigma for (k,N) in lc_ts["cj"]]
                        ,mu_c_ttt = [ N.mu for (k,N) in lc_ttt["cj"]]
                        ,sigma_c_ttt = [ N.sigma for (k,N) in lc_ttt["cj"]]
                        ,time_c = [ k for (k,N) in lc_ts["cj"]]
                        )
        info && println(lc_ttt["aj"][end][2]," ", lc_ttt["bj"][end][2], " ",lc_ttt["cj"][end][2])

        CSV.write("../img/Datos/SV_same_strength.csv", df; header=true)
        @test true
    end

    @testset "same_strength_two_groups" begin

        for j in 1:3
            predicciones_mle = Float64[]
            predicciones_aiaj = Float64[]
            predicciones_bibj = Float64[]
            predicciones_aibi = Float64[]
            predicciones_bici = Float64[]
            predicciones_ajbj = Float64[]
            predicciones_bjcj = Float64[]
            events = [ [["aj"],["bj"]], [["bj"],["cj"]], [["cj"],["aj"]],[["aj"],["bj"]], [["bj"],["cj"]], [["cj"],["aj"]],
                        [["ai"],["bi"]], [["bi"],["ci"]], [["ci"],["ai"]], [["ai"],["bi"]], [["bi"],["ci"]], [["ci"],["ai"]],
                        [["ai"],["aj"]] ]
            results = [[0,1],[0,1],[0,1],[0,1],[0,1],[0,1], [0,1],[0,1],[0,1],[0,1],[0,1],[0,1], [1,0]]
            #batches = [1,2,3,4,5,6,7,8,9,10,11,12,13]
            batches = [1,1,1,1,1,1,1,1,1,1,1,1,1]
            Nbeta = ttt.Gaussian(0.0,1.)
            casos = [100,100,100]
            if j > 1
                events = vcat(events,events)
                results = vcat(results,results)
                batches = vcat(batches,batches)
            end
            if j > 2
                events = vcat(events,events)
                results = vcat(results,results)
                batches = vcat(batches,batches)
            end
            for i in 1:casos[j]
                #println(i)
                if j > 1
                    push!(events, [["ai"],["aj"]])
                    push!(results, [0,1])
                    push!(batches, 1)
                end
                if j > 2
                    push!(events, [["ai"],["aj"]])
                    push!(results, [0,1])
                    push!(batches, 1)
                    push!(events, [["ai"],["aj"]])
                    push!(results, [0,1])
                    push!(batches, 1)
                end
                push!(events, [["ai"],["aj"]])
                push!(results, [0,1])
                push!(batches, 1)
                priors = Dict{String,ttt.Rating}()
                for k in ["aj", "bj", "cj", "ai", "bi", "ci"]
                    priors[k] = ttt.Rating(25., 6.0, 1., 0.0)
                end
                h = ttt.History(events, results, batches, priors, ttt.Environment(iter=iteration))
                ttt.convergence(h, info)

                lc = ttt.learning_curves(h)
                push!(predicciones_mle, i/(1.0+i))
                push!(predicciones_aiaj, 1-ttt.cdf(lc["ai"][1][2]+Nbeta - lc["aj"][1][2]+Nbeta, 0.))
                push!(predicciones_bibj, 1-ttt.cdf(lc["bi"][1][2]+Nbeta - lc["bj"][1][2]+Nbeta, 0.))
                push!(predicciones_aibi, 1-ttt.cdf(lc["ai"][1][2]+Nbeta - lc["bi"][1][2]+Nbeta, 0.))
                push!(predicciones_bici, 1-ttt.cdf(lc["bi"][1][2]+Nbeta - lc["ci"][1][2]+Nbeta, 0.))
                push!(predicciones_ajbj, 1-ttt.cdf(lc["aj"][1][2]+Nbeta - lc["bj"][1][2]+Nbeta, 0.))
                push!(predicciones_bjcj, 1-ttt.cdf(lc["bj"][1][2]+Nbeta - lc["cj"][1][2]+Nbeta, 0.))
            end
            df = DataFrame(mle = predicciones_mle,
                            aiaj = predicciones_aiaj,
                            bibj = predicciones_bibj,
                            aibi = predicciones_aibi,
                            bici = predicciones_bici)
            CSV.write("../img/Datos/SV_same_strength_two_groups_$j.csv", df; header=true)
        end
        @test true
    end

    @testset "Best gamma" begin
        # no le habia agregado 25?
        function skill(exp::Int64, alpha::Float64=0.133)
            return exp^alpha - 1 +25.
        end
        mean_agent = [skill(i) for i in 1:1000]
        beta = 1.
        ev = -1000
        Random.seed!(1)

        mean_target = [(Random.randn(1)[1]*beta + skill(i)) for i in 1:1000]
        perf_target = [(Random.randn(1)[1]*beta + mean_target[i]) for i in 1:1000]
        perf_agent = [(Random.randn(1)[1]*beta + mean_target[i]) for i in 1:1000]
        events = [ [["a"], [string(i)] ] for i in 1:1000]
        results = [ perf_agent[i] > perf_target[i] ? [0,1] : [1,0] for i in 1:1000 ]
        batches= [i for i in 1:1000 ]

        #selected_gammas = [0.005,0.01,0.015,0.02,0.025]
        selected_gammas = [0.005,0.015,0.1,0.55,1.0]
        #gammas = [gamma for gamma in 0.001:0.001:0.04]
        gammas = [gamma for gamma in range(0.001,stop=0.01,length=14)]
        gammas[7] = 0.005
        gamma2 = [gamma for gamma in range(0.01,stop=0.1,length=13)]
        gamma2[2] = 0.015
        gamma3 = [gamma for gamma in range(0.1,stop=1,length=13)]
        gammas = cat(gammas,gamma2,dims =(1, 1))
        gammas = cat(gammas,gamma3,dims =(1, 1))
        evidencias_ts = Float64[]
        evidencias_ttt = Float64[]
        learning_curves = Vector{Vector{Float64}}()
        info && println(gammas)
        for gamma in gammas#gamma=0.015
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

        @test 0.015 == gammas[argmax(evidencias_ttt)]
        df = DataFrame(gammas = gammas
                        ,evidencias_ts = evidencias_ts/ev
                        ,evidencias_ttt = evidencias_ttt/ev)
        CSV.write("../img/Datos/SV_best_gamma_evidences.csv", df; header=true)

        df = DataFrame(mean_agent = mean_agent
                        ,lc_0005 = learning_curves[1]
                        ,lc_0015  = learning_curves[2]
                        ,lc_01 = learning_curves[3]
                        ,lc_01bis = learning_curves[4] #esta repetido....
                        ,lc_05 = learning_curves[5]
                        ,lc_1 = learning_curves[6])
        CSV.write("../img/Datos/SV_best_gamma_lc.csv", df; header=true)
    end

end
