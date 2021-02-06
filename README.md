# Tesis de Licenciatura de Matias Mazzanti


[PDF - Tesis de Licenciatura](https://github.com/mmazz/Analisis_go/blob/master/tesis/main.pdf)

## Requisitos
- Julia 1.5.1 en adelante
- Python 3

## Utilizacion
El make dentro de la carpeta img es el encargado de correr todo lo necesario para generar las figuras correspondientes a la tesis.
- Por el momento correr por primera vez el make, tarda en el orden de los 52 minutos.
- En caso de querer realizar un make desde cero, correr primero make clean dentro de la carmeta img y luego correr make.

## Scripts
Los scrpits dentro de la carpeta Analisis, son los responsables en la utilziacion del metodo
TrueSkill y TTT para los diferentes analisis.

- Summary_filtered.py - Filtra el archivo KGS.csv descargado. Los analisis se realizan con este filtro.
- Los demas archivos de Python realizan las figuras utilizando los CSV de los diferentes scripts de julia.
Los scripts de python se pueden dividir en dos grandes grupos, por un  lado los que generan figuras de resultados y los que no.
- Figuras intro y mas: elo, draw, evidence, gaussian, trueskill, trueskill_ej, data, synthetic_model y synthetic_validation
- Figuras resultados: estimations_H.py, handicap_fit.py, lc.py, study_diff_rank.py y study_same_rank.py.
- estimations_H.py estima la cantidad de handicaps que faltaron asignar y realiza diferentes analisis para probar la efectividad del metodo.

### Julia
- synthetic son los repsonables del analiss para la seccion Validacion.
- Rela_beta_sigma_BestGamma.jl realiza barrido en el parametro gamma para distintas relaciones de los parametros beta y sigma para buscar maximizar la evidencia. A su vez utilizando la mejor relacion compara el metodo TS con TTT y 3 implementaciones distintas de este ultimo. TTT con handicap, sin handicap y handicap sin considerar H1.
- TTT_handicap_fit.jl utiliza el metodo TTT con la mejor relacion y mejor gamma encontrado en el analisis anterior. Se encuentra la relacion lineal y se vuelve a correr para modificar la pendiente por pendiente uno.

- El archivo  genera cuantro nuevos archivos CSV los cuales son un set de datos de entrenamientos y otro set de datos de estudio para el caso con handicap y otro
sin handicap.
- TrainSet_diffRank.jl y  TrainSet_sameRank.jl utilizan unos sets de datos de entrenamientos provenientes de Sets_Training_Study.py. Con ello se prosigue a estimar los datos de prueba mediante sus respectivos scripts de Python.
