all: intro

SV_ev2.csv: ./SV_ev2.csv
	julia ../Analisis/sv2.jl

intro: SV_ev2.csv
	python ./sv2.py


clean:
	rm -f *.csv *.pdf ./Datos/*.csv *.tar.gz
