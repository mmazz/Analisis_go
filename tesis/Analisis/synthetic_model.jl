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
ev = -1000
@testset "Modelo Sintetico" begin

    function rendimiento(x,mu,sigma)
        y = (1/(sigma*(sqrt(2*pi))))*exp(-0.5*((x-mu)/sigma)^2)
        return y
    end

    LENG = 1000

    Jugador_test = "25"
    Jugador_test_2 = "49"
    mean_agent = []
    mean_agent_2 = []
    MU = 25.0
    BETA = 1.0
    SIGMA = 6.0
    actualizacion_num_partidas = 50
    valor_actualizacion = 1
    numero_partidas = 1000
    numero_de_jugadores = 50

    Jugadores = Dict{String,Array{Float32,1}}()

    # Genero jugadores con habilidad aleatoria
    Random.seed!(1)
    for i = 1:1:numero_de_jugadores
        Jugadores[string(i)] = [rand(Uniform(MU-2*BETA,MU+2*BETA)),0]
    end
    # un beta de dif? o dos?
    Jugadores[Jugador_test] = [26.5,0]
    Jugadores[Jugador_test_2] = [25.5,0]
    jugador1 =  []
    jugador2 =  []
    player2_win = []
    jugador1_real_skill = []
    jugador2_real_skill = []

    # Genero las partidas
    for i in 1:1:numero_partidas
        Jugadores_key = collect(keys(Jugadores))
        player1_key = Jugadores_key[rand(1:length(Jugadores_key))]
        Jugadores_pop = copy(Jugadores)
        pop!(Jugadores_pop, player1_key)
        Jugadores_key_pop = collect(keys(Jugadores_pop))
        player2_key = Jugadores_key_pop[rand(1:length(Jugadores_key_pop))]
        player1_rend = Random.randn(1).*BETA.+Jugadores[player1_key][1]
        player2_rend = Random.randn(1).*BETA.+Jugadores[player2_key][1]
        diff = player1_rend - player2_rend
        if diff[1] > 0.0
            diff[1] = 1 # 1 de que perdio negro
        else
            diff[1] = 0
        end
        push!(jugador1,player1_key)
        push!(jugador1_real_skill,Jugadores[player1_key][1])
        push!(jugador2,player2_key)
        push!(jugador2_real_skill,Jugadores[player2_key][1])
        push!(player2_win,Int64(diff[1]))
        # Guardo la info de la habilidad de un solo jugador para comparar despues
        if player2_key == Jugador_test
            push!(mean_agent, Jugadores[player2_key][1])
        elseif player1_key == Jugador_test
            push!(mean_agent, Jugadores[player1_key][1])
        end
        if player2_key == Jugador_test_2
            push!(mean_agent_2, Jugadores[player2_key][1])
        elseif player1_key == Jugador_test_2
            push!(mean_agent_2, Jugadores[player1_key][1])
        end
    end

    data = Dict{Any, Any}("white"=> jugador1, "black"=> jugador2, "white_skill"=> jugador1_real_skill,
            "black_skill"=> jugador2_real_skill, "black_win"=> player2_win)
    df = DataFrame(data)
    CSV.write("../img/Datos/SM_simulacion_constante.csv", df; header=true)

# #=
    @testset "Mu" begin
        println("Mu")
        df= CSV.read("../img/Datos/SM_simulacion_constante.csv")
        LENG = 1000

        len_gammas = 20
        gammas_usados = []
        evidencias_usadas = []
        evidencias_ttt = []
        evidencias_usadas_ts = []
        lc_1 = Vector{Vector{Float64}}()
        lc_2 = Vector{Vector{Float64}}()
        lc_1_ttt = Vector{Vector{Float64}}()
        lc_2_ttt = Vector{Vector{Float64}}()
        lc_1_ttt_last = Float64[]
        lc_2_ttt_last = Float64[]
        predicciones_2025 = Float64[]
        Nbeta = ttt.Gaussian(0.0,1.0)
        mu = [0.0,12.5,25.0]
        sigma = [3.0,3.0,3.0]
        beta = [1.0,1.0,1.0]

        for j = 1:1:length(mu)
            Random.seed!(1)
            results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(df) ]
            events = [[[string(r.white)],[string(r.black)]]  for r in eachrow(df) ]
            times = Vector{Int64}()

            gammas = [gamma for gamma in range(0.000000001,stop=0.0000001,length=len_gammas)]
            evidencias_gamma_ts = Float64[]
            evidencias_gamma_ttt = Float64[]
            EL_gamma = 0.0000001
            push!(gammas_usados, EL_gamma)

            prior_dict = Dict{String,ttt.Rating}()
            for key in Set([(row.white) for row in eachrow(df)])
                prior_dict[string(key)] = ttt.Rating(mu[j],sigma[j],beta[j],EL_gamma)
            end

            results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(df) ]
            composition = [[[string(r.white)],[string(r.black)]]  for r in eachrow(df) ]
            times = Vector{Int64}()
            evidence_ts = Float64[]
            evidence_ttt = Float64[]
            env = ttt.Environment(gamma=EL_gamma,iter=iteration)
            h = ttt.History(composition, results, times, prior_dict, env)
            push!(evidencias_usadas_ts, ttt.log_evidence(h))
            push!(lc_1, [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]] )
            push!(lc_2, [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test_2]] )
            push!(lc_1_ttt, [])
            push!(lc_2_ttt, [])
            #println("Vuelta numero ", j)

            for i in 1:1:numero_partidas
                if Jugador_test in composition[:][i:i][1][1] || Jugador_test in composition[:][i:i][1][2]
                    info && print(i,", ")
                    h = ttt.History(composition[:][1:i], results[:][1:i], times, prior_dict, env)
                    ttt.convergence(h, info)
                    LC_1 = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]]
                    push!(lc_1_ttt[j], LC_1[end])
                end

            end

            h = ttt.History(composition, results, times, prior_dict, env)
            ttt.convergence(h, info)
            lc = ttt.learning_curves(h)
            push!(predicciones_2025, 1-ttt.cdf(lc[Jugador_test][1][2]+Nbeta - lc[Jugador_test_2][1][2]+Nbeta, 0.))

            LC_1 = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]]
            LC_2 = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test_2]]

            push!(lc_1_ttt_last, LC_1[end])
            push!(lc_2_ttt_last, LC_2[end])

            push!(evidencias_usadas, ttt.log_evidence(h))
            info && println("Gamma optimo: ", EL_gamma," | ", ttt.log_evidence(h))

        end

        df = DataFrame(mean_agent = mean_agent
                        ,ts_0 = lc_1[1]
                        ,ttt_0  = lc_1_ttt[1]
                        ,ts_12_5 = lc_1[2]
                        ,ttt_12_5 = lc_1_ttt[2]
                        ,ts_25 = lc_1[3]
                        ,ttt_25  = lc_1_ttt[3]
                        )
        CSV.write("../img/Datos/SM_mu_lc.csv", df; header=true)
        df = DataFrame(mean_agent = mean_agent_2
                        ,ts_0 = lc_2[1]
                        ,ts_12_5 = lc_2[2]
                        ,ts_25 = lc_2[3]

                        )
        CSV.write("../img/Datos/SM_mu_lc_20.csv", df; header=true)

        data = Dict{Any, Any}("Mu"=> mu, "Sigma"=> sigma, "Beta"=> beta,
                "Mu 1"=> lc_1_ttt_last,"Mu 2" => lc_2_ttt_last,
                "Probabilidad" => predicciones_2025,
                "Gamma"=> round.(gammas_usados,sigdigits=8),
                "Evidencia_ttt"=> round.(evidencias_usadas,sigdigits=8)/ev,
                "Evidencia_ts"=> round.(evidencias_usadas_ts,sigdigits=8)/ev)
        df = DataFrame(data)
        CSV.write("../img/Datos/SM_evidencia_mu.csv", df; header=true)
    end


@testset "Sigma Online" begin
    println(" ")
    println("Sigma Online")
    df= CSV.read("../img/Datos/SM_simulacion_constante.csv")
    LENG = 1000
    len_gammas = 20
    gammas_usados = []
    evidencias_usadas = []
    evidencias_ttt = []
    evidencias_usadas_ts = []
    lc_1 = Vector{Vector{Float64}}()
    lc_2 = Vector{Vector{Float64}}()
    lc_1_ttt = Vector{Vector{Float64}}()
    lc_1_ttt_sigma = Vector{Vector{Float64}}()

    lc_1_ttt_mu = Float64[]
    lc_2_ttt_mu = Float64[]
    lc_1_ttt_sigma_final = Float64[]
    lc_2_ttt_sigma_final = Float64[]
    mu = [25.0,25.0,25.0]
    sigma = [0.005,3.0,10.0]
    beta = [1.0,1.0,1.0]
    gamma = [0.25,0.000001,0.0000001]

    for j = 1:1:length(mu)
        Random.seed!(1)
        results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(df) ]
        events = [[[string(r.white)],[string(r.black)]]  for r in eachrow(df) ]
        times = Vector{Int64}()
        evidencias_gamma_ts = Float64[]
        evidencias_gamma_ttt = Float64[]

        EL_gamma = gamma[j]
        push!(gammas_usados, EL_gamma)
        prior_dict = Dict{String,ttt.Rating}()
        for key in Set([(row.white) for row in eachrow(df)])
            prior_dict[string(key)] = ttt.Rating(mu[j],sigma[j],beta[j],EL_gamma)
        end

        results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(df) ]
        composition = [[[string(r.white)],[string(r.black)]]  for r in eachrow(df) ]
        times = Vector{Int64}()
        evidence_ts = Float64[]
        evidence_ttt = Float64[]
        env = ttt.Environment(gamma=EL_gamma,iter=iteration)
        h = ttt.History(composition, results, times, prior_dict, env)
        ttt.convergence(h, info)
        info && println("Gamma optimo: ", EL_gamma," | ", ttt.log_evidence(h))

        push!(evidencias_usadas_ts, ttt.log_evidence(h))

        push!(lc_1_ttt, [])
        push!(lc_1_ttt_sigma, [])
        info && println(1)
        info && println("Vuelta numero ", j)

        for i in 1:1:numero_partidas
            if Jugador_test in composition[:][i:i][1][1] || Jugador_test in composition[:][i:i][1][2]
                info && print(i,", ")
                h = ttt.History(composition[:][1:i], results[:][1:i], times, prior_dict, env)
                ttt.convergence(h, info)
                LC_1 = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]]
                push!(lc_1_ttt[j], LC_1[end])
                LC_1_sigma = [r.sigma for (t, r) in ttt.learning_curves(h)[Jugador_test]]
                push!(lc_1_ttt_sigma[j], LC_1_sigma[end])
            end

        end

        h = ttt.History(composition, results, times, prior_dict, env)
        push!(lc_1, [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]] )
        push!(lc_2, [r.sigma for (t, r) in ttt.learning_curves(h)[Jugador_test]] )
        ttt.convergence(h, info)
        LC_1 = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]]
        LC_2 = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test_2]]
        push!(lc_1_ttt_mu, LC_1[end])
        push!(lc_2_ttt_mu, LC_2[end])
        LC_1 = [r.sigma for (t, r) in ttt.learning_curves(h)[Jugador_test]]
        LC_2 = [r.sigma for (t, r) in ttt.learning_curves(h)[Jugador_test_2]]
        push!(lc_1_ttt_sigma_final, LC_1[end])
        push!(lc_2_ttt_sigma_final, LC_2[end])
        push!(evidencias_usadas, ttt.log_evidence(h))

        info && println("Gamma optimo: ", EL_gamma," | ", ttt.log_evidence(h))

    end

    df = DataFrame(ts_0001 = lc_2[1]
                    ,ttt_0001  = lc_1_ttt_sigma[1]
                    ,ts_3 = lc_2[2]
                    ,ttt_3 = lc_1_ttt_sigma[2]
                    ,ts_10 = lc_2[3]
                    ,ttt_10  = lc_1_ttt_sigma[3]
                    )
    CSV.write("../img/Datos/SM_sigma_lc_online.csv", df; header=true)
    df = DataFrame(mean_agent = mean_agent
                    ,ts_0001 = lc_1[1]
                    ,ttt_0001  = lc_1_ttt[1]
                    ,ts_3 = lc_1[2]
                    ,ttt_3 = lc_1_ttt[2]
                    ,ts_10 = lc_1[3]
                    ,ttt_10  = lc_1_ttt[3]
                    )
    CSV.write("../img/Datos/SM_sigma_lc_mu_online.csv", df; header=true)

    data = Dict{Any, Any}("Mu"=> mu, "Sigma"=> sigma, "Beta"=> beta,
            "Mu 1"=> lc_1_ttt_mu,"Mu 2" => lc_2_ttt_mu,
            "Sigma 1"=> lc_1_ttt_sigma_final,"Sigma 2" => lc_2_ttt_sigma_final,
            "Gamma"=> round.(gammas_usados,sigdigits=8),
            "Evidencia_ttt"=> round.(evidencias_usadas,sigdigits=8)/ev,
            "Evidencia_ts"=> round.(evidencias_usadas_ts,sigdigits=8)/ev)
    df = DataFrame(data)
    CSV.write("../img/Datos/SM_evidencia_sigma_online.csv", df; header=true)

end
# =#
##=
# faltaria hacer un barrido mejor en gamma
    @testset "Sigma" begin
        println(" ")
        println("Sigma")
        df= CSV.read("../img/Datos/SM_simulacion_constante.csv")
        LENG = 1000

        len_gammas = 20
        gammas_usados = []
        evidencias_usadas = []
        evidencias_usadas_ts = []
        lc_sigma = Vector{Vector{Float64}}()
        lc_mu = []
        lc_mu_2 = []
        mu = [25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0]
        sigma = [0.005,0.01,0.5,0.9,1.0,1.2,1.5,2.0,3.0,20.0]
        beta = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
        predicciones_2025 = Float64[]
        gamma = [0.3,0.3,0.000001,0.000001,0.0000001,0.0000001,0.0000001,0.0000001,0.0000001,0.0000000001]
        for j = 1:1:length(mu)
            Nbeta = ttt.Gaussian(0.0,beta[j])
            Random.seed!(1)
            results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(df) ]
            events = [[[string(r.white)],[string(r.black)]]  for r in eachrow(df) ]
            times = Vector{Int64}()
            evidencias_gamma_ts = Float64[]
            evidencias_gamma_ttt = Float64[]
            EL_gamma = gamma[j]

            prior_dict = Dict{String,ttt.Rating}()
            for key in Set([(row.white) for row in eachrow(df)])
                prior_dict[string(key)] = ttt.Rating(mu[j],sigma[j],beta[j],EL_gamma)
            end

            results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(df) ]
            composition = [[[string(r.white)],[string(r.black)]]  for r in eachrow(df) ]
            times = Vector{Int64}()
            evidence_ts = Float64[]
            evidence_ttt = Float64[]

            env = ttt.Environment(gamma=EL_gamma,iter=iteration)
            h = ttt.History(composition, results, times, prior_dict, env)
            push!(evidencias_usadas_ts, ttt.log_evidence(h))

            ttt.convergence(h, info)
            LC = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]]
            LC_2 = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test_2]]
            push!(lc_mu, LC[end] )
            push!(lc_mu_2, LC_2[end] )
            push!(evidencias_usadas, ttt.log_evidence(h))
            println("Sigma ",sigma[j] ," Gamma optimo: ", EL_gamma," | ",ttt.log_evidence(h))
            lc = ttt.learning_curves(h)
            push!(predicciones_2025, 1-ttt.cdf(lc[Jugador_test][1][2]+Nbeta - lc[Jugador_test_2][1][2]+Nbeta, 0.))

        end
        #Podria guardarme los posterios de los jugadores, deberian dar los mismos
        # Para los que tienen evidencia similares
        #w_mean = [ ttt.posterior(h.batches[r], string(data[r,"white"])).mu for r in 1:size(data)[1]]
        data = Dict{Any, Any}("Mu"=> mu, "Sigma"=> sigma, "Beta"=> beta,
                "Mu 1" => lc_mu, " Mu 2" => lc_mu_2,
                "Gamma"=> round.(gamma,sigdigits=2),
                "Evidencia_ttt"=> round.(evidencias_usadas,sigdigits=4)/ev,
                "Evidencia_ts"=> round.(evidencias_usadas_ts,sigdigits=4)/ev,
                "proba_20vs25"=> round.(predicciones_2025,sigdigits=3))
        df = DataFrame(data)
        CSV.write("../img/Datos/SM_evidencia_sigma.csv", df; header=true)
    end
# =#
    @testset "Beta Online" begin

        println(" ")
        println("Beta Online")
        df= CSV.read("../img/Datos/SM_simulacion_constante.csv")
        LENG = 1000

        len_gammas = 20
        gammas_usados = []
        evidencias_usadas = []
        evidencias_ttt = []
        evidencias_usadas_ts = []
        lc_1 = Vector{Vector{Float64}}()
        lc_2 = Vector{Vector{Float64}}()
        lc_1_ttt = Vector{Vector{Float64}}()
        lc_1_ttt_sigma = Vector{Vector{Float64}}()
        predicciones= Float64[]
        lc_1_ttt_mu = Float64[]
        lc_2_ttt_mu = Float64[]
        lc_1_ttt_sigma_final = Float64[]
        lc_2_ttt_sigma_final = Float64[]
        mu = [25.0,25.0,25.0,25.0,25.0]
        beta = [0.1,1.0,5.0,10.0,100.0]
        sigma = beta.*3.0
        gamma = [0.000001,0.000001,0.000001,0.000001,0.000001]

        for j = 1:1:length(mu)
            Random.seed!(1)
            Nbeta = ttt.Gaussian(0.0,beta[j])
            results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(df) ]
            events = [[[string(r.white)],[string(r.black)]]  for r in eachrow(df) ]
            times = Vector{Int64}()
            evidencias_gamma_ts = Float64[]
            evidencias_gamma_ttt = Float64[]

            EL_gamma = gamma[j]
            push!(gammas_usados, EL_gamma)
            prior_dict = Dict{String,ttt.Rating}()
            for key in Set([(row.white) for row in eachrow(df)])
                prior_dict[string(key)] = ttt.Rating(mu[j],sigma[j],beta[j],EL_gamma)
            end

            results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(df) ]
            composition = [[[string(r.white)],[string(r.black)]]  for r in eachrow(df) ]
            times = Vector{Int64}()
            evidence_ts = Float64[]
            evidence_ttt = Float64[]
            env = ttt.Environment(gamma=EL_gamma,iter=iteration)
            h = ttt.History(composition, results, times, prior_dict, env)
            ttt.convergence(h, info)
            info && println("Gamma optimo: ", EL_gamma," | ", ttt.log_evidence(h))
            push!(evidencias_usadas_ts, ttt.log_evidence(h))
            push!(lc_1_ttt, [])
            push!(lc_1_ttt_sigma, [])
            info && println(1)
            info && println("Vuelta numero ", j)

            for i in 1:1:numero_partidas
                if Jugador_test in composition[:][i:i][1][1] || Jugador_test in composition[:][i:i][1][2]
                    info && print(i,", ")
                    h = ttt.History(composition[:][1:i], results[:][1:i], times, prior_dict, env)
                    ttt.convergence(h, info)
                    LC_1 = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]]
                    push!(lc_1_ttt[j], LC_1[end])
                end
            end

            h = ttt.History(composition, results, times, prior_dict, env)
            push!(lc_1, [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]] )
            ttt.convergence(h, info)
            LC_1 = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]]
            LC_2 = [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test_2]]
            push!(lc_1_ttt_mu, LC_1[end])
            push!(lc_2_ttt_mu, LC_2[end])
            LC_1 = [r.sigma for (t, r) in ttt.learning_curves(h)[Jugador_test]]
            LC_2 = [r.sigma for (t, r) in ttt.learning_curves(h)[Jugador_test_2]]
            push!(lc_1_ttt_sigma_final, LC_1[end])
            push!(lc_2_ttt_sigma_final, LC_2[end])
            push!(evidencias_usadas, ttt.log_evidence(h))
            lc = ttt.learning_curves(h)
            push!(predicciones, 1-ttt.cdf(lc[Jugador_test][1][2]+Nbeta - lc[Jugador_test_2][1][2]+Nbeta, 0.))
            info && println("Gamma optimo: ", EL_gamma," | ", ttt.log_evidence(h))

        end

        df = DataFrame(mean_agent = mean_agent
                        ,ts_01 = lc_1[1]
                        ,ttt_01  = lc_1_ttt[1]
                        ,ts_1 = lc_1[2]
                        ,ttt_1 = lc_1_ttt[2]
                        ,ts_5 = lc_1[3]
                        ,ttt_5  = lc_1_ttt[3]
                        ,ts_10 = lc_1[4]
                        ,ttt_10  = lc_1_ttt[4]
                        ,ts_100 = lc_1[5]
                        ,ttt_100  = lc_1_ttt[5]
                        )
        CSV.write("../img/Datos/SM_beta_lc_mu_online.csv", df; header=true)

        data = Dict{Any, Any}("Mu"=> mu, "Sigma"=> sigma, "Beta"=> beta,
                "Mu 1"=> lc_1_ttt_mu,"Mu 2" => lc_2_ttt_mu,
                "Sigma 1"=> lc_1_ttt_sigma_final,"Sigma 2" => lc_2_ttt_sigma_final,
                "Gamma"=> round.(gammas_usados,sigdigits=8),
                "Evidencia_ttt"=> round.(evidencias_usadas,sigdigits=8)/ev,
                "Evidencia_ts"=> round.(evidencias_usadas_ts,sigdigits=8)/ev,
                "proba_1vs2"=> round.(predicciones,sigdigits=3))

        df = DataFrame(data)
        CSV.write("../img/Datos/SM_evidencia_proba_beta.csv", df; header=true)

    end

end





############################  FIN ########################################


#=
    @testset "Beta" begin
        # En este mostrar que no cambia nada mas que la escala relativa.
        # Guardarme todos los mus, y ver la resta, pero ver que da igual la
        # Proba de ganar.
        println(" ")
        println("Beta")
        df= CSV.read("./Datos/SM_simulacion_constante.csv")
        LENG = 1000
        iteraciones = 100
        len_gammas = 20
        gammas_usados = []
        evidencias_usadas = []
        evidencias_usadas_ts = []
        lc_1 = Vector{Vector{Float64}}()
        lc_2 = Vector{Vector{Float64}}()
        mu = [25.0,25.0,25.0,25.0,25.0,25.0]
        beta = [0.1,1.0,5.0,10.0,100.0,1000.0]
        sigma = beta.*6.0
        predicciones_2025 = Float64[]
        for j = 1:1:length(mu)
            Nbeta = ttt.Gaussian(0.0,beta[j])
            Random.seed!(1)
            results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(df) ]
            events = [[[string(r.white)],[string(r.black)]]  for r in eachrow(df) ]
            times = Vector{Int64}()

            #=
            gammas = [gamma for gamma in range(0.0000000001,stop=0.00000001,length=len_gammas)]
            evidencias_gamma_ts = Float64[]
            evidencias_gamma_ttt = Float64[]
            #Primer pasada de gammas
            for gamma_i in gammas
                prior_dict = Dict{String,ttt.Rating}()
                for key in Set([(row.white) for row in eachrow(df)])
                    prior_dict[string(key)] = ttt.Rating(mu[j],sigma[j],beta[j],gamma_i)
                end
                env=ttt.Environment(gamma=gamma_i,iter=iteraciones)
                h = ttt.History(events, results, times, prior_dict, env)
                push!(evidencias_gamma_ts, ttt.log_evidence(h))
                ttt.convergence(h)
                push!(evidencias_gamma_ttt, ttt.log_evidence(h))
            end
            EL_gamma = gammas[argmax(evidencias_gamma_ttt)]

            =#
            EL_gamma = 0.0001
            push!(gammas_usados, EL_gamma)
            prior_dict = Dict{String,ttt.Rating}()
            for key in Set([(row.white) for row in eachrow(df)])
                prior_dict[string(key)] = ttt.Rating(mu[j],sigma[j],beta[j],EL_gamma)
            end

            results = [row.black_win == 0 ? [1,0] : [0, 1] for row in eachrow(df) ]
            composition = [[[string(r.white)],[string(r.black)]]  for r in eachrow(df) ]
            times = Vector{Int64}()
            evidence_ts = Float64[]
            evidence_ttt = Float64[]

            env = ttt.Environment(gamma=EL_gamma,iter=iteraciones)
            h = ttt.History(composition, results, times, prior_dict, env)
            push!(evidencias_usadas_ts, ttt.log_evidence(h))
            push!(lc_1, [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]] )
            push!(lc_2, [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test_2]] )
            ttt.convergence(h)
            push!(lc_1, [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test]] )
            push!(lc_2, [r.mu for (t, r) in ttt.learning_curves(h)[Jugador_test_2]] )

            push!(evidencias_usadas, ttt.log_evidence(h))
            println("Gamma optimo: ", EL_gamma," | ", ttt.log_evidence(h))
            lc = ttt.learning_curves(h)
            push!(predicciones_2025, 1-ttt.cdf(lc[Jugador_test_2][1][2]+Nbeta - lc[Jugador_test][1][2]+Nbeta, 0.))


        end

        df = DataFrame(mean_agent = mean_agent
                        ,ts_01 = lc_1[1]
                        ,ttt_01  = lc_1[2]
                        ,ts_1 = lc_1[3]
                        ,ttt_1 = lc_1[4]
                        ,ts_5 = lc_1[5]
                        ,ttt_5 = lc_1[6]
                        ,ts_10 = lc_1[7]
                        ,ttt_10 = lc_1[8]
                        ,ts_100 = lc_1[9]
                        ,ttt_100 = lc_1[10]
                        ,ts_1000 = lc_1[11]
                        ,ttt_1000 = lc_1[12]
                        )
        CSV.write("./Datos/SM_beta_lc_25.csv", df; header=true)
        df = DataFrame(mean_agent = mean_agent_2
                        ,ts_01 = lc_2[1]
                        ,ttt_01  = lc_2[2]
                        ,ts_1 = lc_2[3]
                        ,ttt_1 = lc_2[4]
                        ,ts_5 = lc_2[5]
                        ,ttt_5  = lc_2[6]
                        ,ts_10 = lc_2[7]
                        ,ttt_10 = lc_2[8]
                        ,ts_100 = lc_2[9]
                        ,ttt_100 = lc_2[10]
                        ,ts_1000 = lc_2[11]
                        ,ttt_1000 = lc_2[12]
                        )
        CSV.write("./Datos/SM_beta_lc_20.csv", df; header=true)

        data = Dict{Any, Any}("Mu"=> mu, "Sigma"=> sigma, "Beta"=> beta,
                "Gamma"=> round.(gammas_usados,sigdigits=8),
                "Evidencia_ttt"=> round.(evidencias_usadas,sigdigits=8),
                "Evidencia_ts"=> round.(evidencias_usadas_ts,sigdigits=8),
                "proba_20vs25"=> predicciones_2025)
        df = DataFrame(data)
        CSV.write("./Datos/SM_evidencia_proba_beta.csv", df; header=true)
    end

     =#
