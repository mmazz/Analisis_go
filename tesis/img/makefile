all: intro julia resultados1 resultados2

KGS.tar.gz:
	wget https://github.com/mmazz/Analisis_go/releases/download/v1.0/KGS.tar.gz
KGS.csv: KGS.tar.gz
	tar -zxvf $<

TTT.tar.gz:
	wget https://github.com/mmazz/Analisis_go/releases/download/v1.1/TTT.tar.gz
TTT_H_uno.csv: TTT.tar.gz
	tar -zxvf ./$<

rela.tar.gz:
	wget https://github.com/mmazz/Analisis_go/releases/download/v1.2/rela.tar.gz
rela_beta_sigma.csv: rela.tar.gz
	tar -zxvf ./$<

TrainingSet.tar.gz:
	wget https://github.com/mmazz/Analisis_go/releases/download/v2.0/TrainingSet.tar.gz
TrainingSet_diffRank_TTT.csv: TrainingSet.tar.gz
	tar -zxvf ./$<


KGS_filtered.csv: KGS.csv
	python ./summary_filtered.py

intro: KGS_filtered.csv
	python ./elo.py
	python ./draw.py
	python ./evidence.py
	python ./gaussian.py
	python ./trueskill.py
	python ./trueskill_ej.py
	python ./data.py

julia: rela_beta_sigma.csv TTT_H_uno.csv TrainingSet_diffRank_TTT.csv
	@echo "*******************************"
	@echo "Se requiere Julia version 1.5.1"
	@echo "*******************************"
	julia ../Analisis/synthetic_validation.jl
	julia ../Analisis/synthetic_model.jl
	python ./synthetic_validation.py
	python ./synthetic_model.py

resultados1:
	python ./rela_beta_sigma.py
	python ./evidence_gamma.py
	python ./handicap_fit.py
	python ./sets_training_study.py
	python ./lc.py
	python ./optimal_H.py
	python ./estimations_H.py
	python ./probability_H.py

resultados2:
	python ./study_same_rank.py
	python ./study_diff_rank.py

clean:
	rm -f *.csv *.pdf ./Datos/*.csv *.tar.gz
