#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue  un  2 16:00:17 2020

@author: mati
black_win es 1 si gano el negro.
"""
import matplotlib.pyplot as plt
import pandas as pd
import os
name = os.path.basename(__file__).split(".py")[0]


df_TTT_h = pd.read_csv('./Datos/TTT_H_analizada.csv')

# analisis de las partidas jugadas
total_partidas = df_TTT_h.shape[0]
partidas_con_H = df_TTT_h.black_win[df_TTT_h.handicap > 1].shape[0]
porcentaje_con_H = round(100*partidas_con_H/total_partidas, 2)

print('Partidas jugadas con Handicap:', porcentaje_con_H, "% de", partidas_con_H, ' Partidas')
print(" ")


partidas_con_H_est = df_TTT_h[df_TTT_h.handicap_prediction > 1].shape[0]
porcentaje_con_H_est = round(100*partidas_con_H_est/total_partidas, 2)

#print('Partidas que estimamos que se deberian jugar sin Handicap:', porcentaje_sin_H_est, "% de", partidas_sin_H_est, ' Partidas')
print('Partidas propuestas con Handicap:', porcentaje_con_H_est, "% de", partidas_con_H_est, ' Partidas')
print(" ")

# las partidas que  deberian tener handicap pero no se le dio, como salieron?
predicciones_coincidencia = df_TTT_h.black_win[(df_TTT_h.handicap_prediction > 1)
                                      & (df_TTT_h.handicap > 1)]
partidas_coincidencia = predicciones_coincidencia.shape[0]
porcentaje_coincidencia = round(100*partidas_coincidencia/partidas_con_H, 2)
# de esas partidas cuantas se ganaron
print('Partidas propuestas y con H coicniden en un',  porcentaje_coincidencia,"%")

predicciones_sin = df_TTT_h.black_win[(df_TTT_h.handicap_prediction > 1)
                                      & (df_TTT_h.handicap == 1)]
partidas_sin_H = predicciones_sin.shape[0]
porcentaje_sin_H = round(100*partidas_sin_H/total_partidas, 2)
# de esas partidas cuantas se ganaron
wins_porcentaje_sin_H = round(100*predicciones_sin.sum()/partidas_sin_H, 2)

print("Partidas con H1 y se estima que deberia Gano negro", wins_porcentaje_sin_H, "% de", partidas_sin_H, ' Partidas')
print(" ")
predicciones_9 = df_TTT_h.black_win[df_TTT_h.handicap == 9]
partidas_9 = predicciones_9.shape[0]
porcentaje_9 = round(100*predicciones_9.sum()/partidas_9, 2)

print("Partidas con H9 y se estima que deberia Gano negro", porcentaje_9, "% de", partidas_9, ' Partidas')
print(" ")

############################################################################
################################### partidas sin H pero que deberian   ######
############################################################################
# Fijamos los handicaps que vamos a usar.
handicaps = [1, 2, 3, 4, 5, 6, 7, 8, 9]
handicaps_bien = [1, 2, 3, 4, 5, 6, 7]
handicaps_color = [-1, -2, -3, -4, -5, -6, -7]
handicaps_mas = [-1, 1, 2, 3, 4, 5, 6, 7]
handicaps_menos = [ 2, 3, 4, 5, 6, 7]
# Asigno los limites a los cinco graficos
ylim = [10, 60]
ylim_bien = [20, 70]
ylim_color = [40, 80]
ylim_mas = [20, 70]
ylim_menos = [20, 60]


def frac_hist(handicaps, porcentajes, heights,  x_ticks=[],ylim=[]):
    fig, ax = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2, 1],
                                              'height_ratios': [1]})
    ax1 = ax[0]
    ax2 = ax[1]

    ax1.plot(handicaps, porcentajes, color='steelblue')
    ax1.scatter(handicaps, porcentajes)
    ax1.axhline(y=50, color='black', linestyle='--', label='Equiprobability')
    ax1.set_xlabel("Proposed handicap value")
    ax1.set_ylabel("Porcentage of winning black")
    ax1.set_ylim(ylim[0], ylim[1])
    ax1.set_xticks(handicaps)
    ax1.legend()
    ax2.bar(handicaps, height=heights, log=True, edgecolor='black')
    ax2.set_xlabel("Proposed handicap value")
    if len(x_ticks) != 0:
        ax2.set_xticks(x_ticks)
    plt.close(fig)
    return fig


def frac_hist_doble(handicaps, porcentajes, porcentajes_acotado, heights,
                    heights_acotados,  x_ticks=[], label='', ylim=[0, 100]):
    fig, ax = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2, 1],
                                              'height_ratios': [1]})
    ax1 = ax[0]
    ax2 = ax[1]

    ax1.scatter(handicaps, porcentajes)
    ax1.plot(handicaps, porcentajes, color='steelblue', label=f'{label} handicap by more \n than one')
    ax1.scatter(handicaps, porcentajes_acotado, color='firebrick')
    ax1.plot(handicaps, porcentajes_acotado, color='firebrick', label=f'{label} handicap by one')
    ax1.axhline(y=50, color='black', linestyle='--', label='Equiprobability')
    ax1.set_xlabel("Proposed handicap value")
    ax1.set_ylabel("Porcentage of winning black")
    ax1.set_xticks(x_ticks)
    ax1.set_ylim(ylim[0], ylim[1])

    ax2.bar(handicaps, height=heights, alpha=0.5,log=True, edgecolor='black')
    ax2.bar(handicaps, height=heights_acotados, alpha=0.5, log=True, color='firebrick', edgecolor='black')
    ax2.set_xlabel("Proposed handicap value")
    if len(x_ticks) != 0:
        ax2.set_xticks(x_ticks)
    ax1.legend()
    plt.close(fig)
    return fig


df_sinH = df_TTT_h[(df_TTT_h.handicap == 1)]
predicciones_1 = df_sinH[(df_sinH.handicap_prediction == 1)]
predicciones_2 = df_sinH[(df_sinH.handicap_prediction == 2)]
predicciones_3 = df_sinH[(df_sinH.handicap_prediction == 3)]
predicciones_4 = df_sinH[(df_sinH.handicap_prediction == 4)]
predicciones_5 = df_sinH[(df_sinH.handicap_prediction == 5)]
predicciones_6 = df_sinH[(df_sinH.handicap_prediction == 6)]
predicciones_7 = df_sinH[(df_sinH.handicap_prediction == 7)]
predicciones_8 = df_sinH[(df_sinH.handicap_prediction == 8)]
predicciones_9 = df_sinH[(df_sinH.handicap_prediction == 9)]

partidas_H1 = predicciones_1.shape[0]
partidas_H2 = predicciones_2.shape[0]
partidas_H3 = predicciones_3.shape[0]
partidas_H4 = predicciones_4.shape[0]
partidas_H5 = predicciones_5.shape[0]
partidas_H6 = predicciones_6.shape[0]
partidas_H7 = predicciones_7.shape[0]
partidas_H8 = predicciones_8.shape[0]
partidas_H9 = predicciones_9.shape[0]

porcentaje_H1 = round(100*predicciones_1.black_win.sum()/partidas_H1, 2)
porcentaje_H2 = round(100*predicciones_2.black_win.sum()/partidas_H2, 2)
porcentaje_H3 = round(100*predicciones_3.black_win.sum()/partidas_H3, 2)
porcentaje_H4 = round(100*predicciones_4.black_win.sum()/partidas_H4, 2)
porcentaje_H5 = round(100*predicciones_5.black_win.sum()/partidas_H5, 2)
porcentaje_H6 = round(100*predicciones_6.black_win.sum()/partidas_H6, 2)
porcentaje_H7 = round(100*predicciones_7.black_win.sum()/partidas_H7, 2)
porcentaje_H8 = round(100*predicciones_8.black_win.sum()/partidas_H8, 2)
porcentaje_H9 = round(100*predicciones_9.black_win.sum()/partidas_H9, 2)

porcentajes = [porcentaje_H1, porcentaje_H2, porcentaje_H3, porcentaje_H4,
               porcentaje_H5, porcentaje_H6, porcentaje_H7, porcentaje_H8, porcentaje_H9]
heights = [partidas_H1, partidas_H2, partidas_H3, partidas_H4, partidas_H5,
           partidas_H6, partidas_H7, partidas_H8, partidas_H9]

h_leng = len(handicaps)

fig = frac_hist(handicaps, porcentajes[:h_leng], heights[:h_leng], handicaps, ylim)
fig.savefig(f'./{name}_noH.pdf', dpi=100)



############################################################################
###################################  Estimacion correctas  ##################
############################################################################
# las partidas que si se le dio handicap correcto como salieron
#df_TTT_h = df_TTT_h[(df_TTT_h.w_std_prior <= 0.5) & (df_TTT_h.b_std_prior <= 0.5)]

predicciones_con_1_bien = df_TTT_h[(df_TTT_h.handicap_prediction == 1)
                                     & (df_TTT_h.handicap == 1)]
# partidas con handicap 2, y que se le asigno bien, 50%
predicciones_con_2_bien = df_TTT_h[(df_TTT_h.handicap_prediction == 2)
                                   & (df_TTT_h.handicap == 2)]
predicciones_con_3_bien = df_TTT_h[(df_TTT_h.handicap_prediction == 3)
                                   & (df_TTT_h.handicap == 3)]
predicciones_con_4_bien = df_TTT_h[(df_TTT_h.handicap_prediction == 4)
                                   & (df_TTT_h.handicap == 4)]
predicciones_con_5_bien = df_TTT_h[(df_TTT_h.handicap_prediction == 5)
                                   & (df_TTT_h.handicap == 5)]
predicciones_con_6_bien = df_TTT_h[(df_TTT_h.handicap_prediction == 6)
                                   & (df_TTT_h.handicap == 6)]
predicciones_con_7_bien = df_TTT_h[(df_TTT_h.handicap_prediction == 7)
                                    & (df_TTT_h.handicap == 7)]
predicciones_con_8_bien = df_TTT_h[(df_TTT_h.handicap_prediction == 8)
                                    & (df_TTT_h.handicap == 8)]

predicciones_con_9_bien = df_TTT_h[(df_TTT_h.handicap_prediction == 9)
                                    & (df_TTT_h.handicap == 9)]

partidas_H1_bien = predicciones_con_1_bien.shape[0]
partidas_H2_bien = predicciones_con_2_bien.shape[0]
partidas_H3_bien = predicciones_con_3_bien.shape[0]
partidas_H4_bien = predicciones_con_4_bien.shape[0]
partidas_H5_bien = predicciones_con_5_bien.shape[0]
partidas_H6_bien = predicciones_con_6_bien.shape[0]
partidas_H7_bien = predicciones_con_7_bien.shape[0]
partidas_H8_bien = predicciones_con_8_bien.shape[0]
partidas_H9_bien = predicciones_con_9_bien.shape[0]

porcentaje_H1_bien = round(100*predicciones_con_1_bien.black_win.sum()/partidas_H1_bien, 2)
porcentaje_H2_bien = round(100*predicciones_con_2_bien.black_win.sum()/partidas_H2_bien, 2)
porcentaje_H3_bien = round(100*predicciones_con_3_bien.black_win.sum()/partidas_H3_bien, 2)
porcentaje_H4_bien = round(100*predicciones_con_4_bien.black_win.sum()/partidas_H4_bien, 2)
porcentaje_H5_bien = round(100*predicciones_con_5_bien.black_win.sum()/partidas_H5_bien, 2)
porcentaje_H6_bien = round(100*predicciones_con_6_bien.black_win.sum()/partidas_H6_bien, 2)
porcentaje_H7_bien = round(100*predicciones_con_7_bien.black_win.sum()/partidas_H7_bien, 2)
porcentaje_H8_bien = round(100*predicciones_con_8_bien.black_win.sum()/partidas_H8_bien, 2)
porcentaje_H9_bien = round(100*predicciones_con_9_bien.black_win.sum()/partidas_H9_bien, 2)

porcentajes_bien = [porcentaje_H1_bien, porcentaje_H2_bien, porcentaje_H3_bien, porcentaje_H4_bien,
               porcentaje_H5_bien, porcentaje_H6_bien, porcentaje_H7_bien, porcentaje_H8_bien, porcentaje_H9_bien]
heights_bien = [partidas_H1_bien, partidas_H2_bien, partidas_H3_bien, partidas_H4_bien, partidas_H5_bien,
           partidas_H6_bien, partidas_H7_bien, partidas_H8_bien, partidas_H9_bien]
h_leng = len(handicaps_bien)
fig = frac_hist(handicaps=handicaps_bien, porcentajes=porcentajes_bien[:h_leng], heights=heights_bien[:h_leng],
                x_ticks=handicaps_bien, ylim=ylim_bien)
fig.savefig(f'./{name}_good.pdf', dpi=100)


############################################################################
###################################  Estimacion color erroneo  ##################
############################################################################
# las partidas que si se le dio handicap correcto como salieron
#df_TTT_h = df_TTT_h[(df_TTT_h.w_std_prior <= 0.5) & (df_TTT_h.b_std_prior <= 0.5)]

predicciones_color_1 = df_TTT_h[(df_TTT_h.handicap_prediction == -1)]
predicciones_color_2 = df_TTT_h[(df_TTT_h.handicap_prediction == -2)]
predicciones_color_3 = df_TTT_h[(df_TTT_h.handicap_prediction == -3)]
predicciones_color_4 = df_TTT_h[(df_TTT_h.handicap_prediction == -4)]
predicciones_color_5 = df_TTT_h[(df_TTT_h.handicap_prediction == -5)]
predicciones_color_6 = df_TTT_h[(df_TTT_h.handicap_prediction == -6)]
predicciones_color_7 = df_TTT_h[(df_TTT_h.handicap_prediction == -7)]
predicciones_color_8 = df_TTT_h[(df_TTT_h.handicap_prediction == -8)]

print('valor de handicap en partidas de color mal asignada', df_TTT_h[df_TTT_h.handicap_prediction < 1].handicap.mean())

partidas_H1_color = predicciones_color_1.shape[0]
partidas_H2_color = predicciones_color_2.shape[0]
partidas_H3_color = predicciones_color_3.shape[0]
partidas_H4_color = predicciones_color_4.shape[0]
partidas_H5_color = predicciones_color_5.shape[0]
partidas_H6_color = predicciones_color_6.shape[0]
partidas_H7_color = predicciones_color_7.shape[0]
partidas_H8_color = predicciones_color_8.shape[0]

porcentaje_H1_color = round(100*predicciones_color_1.black_win.sum()/partidas_H1_color, 2)
porcentaje_H2_color = round(100*predicciones_color_2.black_win.sum()/partidas_H2_color, 2)
porcentaje_H3_color = round(100*predicciones_color_3.black_win.sum()/partidas_H3_color, 2)
porcentaje_H4_color = round(100*predicciones_color_4.black_win.sum()/partidas_H4_color, 2)
porcentaje_H5_color = round(100*predicciones_color_5.black_win.sum()/partidas_H5_color, 2)
porcentaje_H6_color = round(100*predicciones_color_6.black_win.sum()/partidas_H6_color, 2)
porcentaje_H7_color = round(100*predicciones_color_7.black_win.sum()/partidas_H7_color, 2)
porcentaje_H8_color = round(100*predicciones_color_8.black_win.sum()/partidas_H8_color, 2)
porcentajes_color = [porcentaje_H1_color, porcentaje_H2_color, porcentaje_H3_color, porcentaje_H4_color,
               porcentaje_H5_color, porcentaje_H6_color, porcentaje_H7_color, porcentaje_H8_color]
heights_color = [partidas_H1_color, partidas_H2_color, partidas_H3_color, partidas_H4_color, partidas_H5_color,
           partidas_H6_color, partidas_H7_color, partidas_H8_color]

h_leng = len(handicaps_color)
fig = frac_hist(handicaps=handicaps_color, porcentajes=porcentajes_color[:h_leng], heights=heights_color[:h_leng],
                 x_ticks=handicaps_color, ylim=ylim_color)
fig.savefig(f'./{name}_color.pdf', dpi=100)



############################################################################
################################### handicap de mas   ####################################
############################################################################
# las partidas que si se le dio handicap pero de mas  como salieron
# es decir la diferencia entre los jugadores era para menos handicap que el dado

# partidas con handicap 2, pero deberian haber tenido menos handicap es decir
# deberia ganar negro

predicciones_con_1_mas = df_TTT_h[(df_TTT_h.handicap_prediction == -1)
                                  & (df_TTT_h.handicap > 1)]
predicciones_con_2_mas = df_TTT_h[(df_TTT_h.handicap_prediction == 1)
                                  & (df_TTT_h.handicap > 2)]
predicciones_con_3_mas = df_TTT_h[(df_TTT_h.handicap_prediction == 2)
                                  & (df_TTT_h.handicap > 3)]
predicciones_con_4_mas = df_TTT_h[(df_TTT_h.handicap_prediction == 3)
                                  & (df_TTT_h.handicap > 4)]
predicciones_con_5_mas = df_TTT_h[(df_TTT_h.handicap_prediction == 4)
                                  & (df_TTT_h.handicap > 5)]
predicciones_con_6_mas = df_TTT_h[(df_TTT_h.handicap_prediction == 5)
                                  & (df_TTT_h.handicap > 6)]
predicciones_con_7_mas = df_TTT_h[(df_TTT_h.handicap_prediction == 6)
                                  & (df_TTT_h.handicap > 7)]
predicciones_con_8_mas = df_TTT_h[(df_TTT_h.handicap_prediction == 7)
                                  & (df_TTT_h.handicap > 8)]

partidas_H1_mas = predicciones_con_1_mas.shape[0]
partidas_H2_mas = predicciones_con_2_mas.shape[0]
partidas_H3_mas = predicciones_con_3_mas.shape[0]
partidas_H4_mas = predicciones_con_4_mas.shape[0]
partidas_H5_mas = predicciones_con_5_mas.shape[0]
partidas_H6_mas = predicciones_con_6_mas.shape[0]
partidas_H7_mas = predicciones_con_7_mas.shape[0]
partidas_H8_mas = predicciones_con_8_mas.shape[0]

porcentaje_H1_mas = round(100*predicciones_con_1_mas.black_win.sum()/partidas_H1_mas, 2)
porcentaje_H2_mas = round(100*predicciones_con_2_mas.black_win.sum()/partidas_H2_mas, 2)
porcentaje_H3_mas = round(100*predicciones_con_3_mas.black_win.sum()/partidas_H3_mas, 2)
porcentaje_H4_mas = round(100*predicciones_con_4_mas.black_win.sum()/partidas_H4_mas, 2)
porcentaje_H5_mas = round(100*predicciones_con_5_mas.black_win.sum()/partidas_H5_mas, 2)
porcentaje_H6_mas = round(100*predicciones_con_6_mas.black_win.sum()/partidas_H6_mas, 2)
porcentaje_H7_mas = round(100*predicciones_con_7_mas.black_win.sum()/partidas_H7_mas, 2)
porcentaje_H8_mas = round(100*predicciones_con_8_mas.black_win.sum()/partidas_H8_mas, 2)

predicciones_con_1_mas_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == -1)
                                                  & (df_TTT_h.handicap == 1)]
predicciones_con_2_mas_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 1)
                                                  & (df_TTT_h.handicap == 2)]
predicciones_con_3_mas_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 2)
                                                  & (df_TTT_h.handicap == 3)]
predicciones_con_4_mas_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 3)
                                                  & (df_TTT_h.handicap == 4)]
predicciones_con_5_mas_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 4)
                                                  & (df_TTT_h.handicap == 5)]
predicciones_con_6_mas_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 5)
                                                  & (df_TTT_h.handicap == 6)]
predicciones_con_7_mas_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 6)
                                                  & (df_TTT_h.handicap == 7)]
predicciones_con_8_mas_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 7)
                                                  & (df_TTT_h.handicap == 8)]

partidas_H1_mas_acotado = predicciones_con_1_mas_acotado.shape[0]
partidas_H2_mas_acotado = predicciones_con_2_mas_acotado.shape[0]
partidas_H3_mas_acotado = predicciones_con_3_mas_acotado.shape[0]
partidas_H4_mas_acotado = predicciones_con_4_mas_acotado.shape[0]
partidas_H5_mas_acotado = predicciones_con_5_mas_acotado.shape[0]
partidas_H6_mas_acotado = predicciones_con_6_mas_acotado.shape[0]
partidas_H7_mas_acotado = predicciones_con_7_mas_acotado.shape[0]
partidas_H8_mas_acotado = predicciones_con_8_mas_acotado.shape[0]

porcentaje_H1_mas_acotado = round(100*predicciones_con_1_mas_acotado.black_win.sum()/partidas_H1_mas_acotado, 2)
porcentaje_H2_mas_acotado = round(100*predicciones_con_2_mas_acotado.black_win.sum()/partidas_H2_mas_acotado, 2)
porcentaje_H3_mas_acotado = round(100*predicciones_con_3_mas_acotado.black_win.sum()/partidas_H3_mas_acotado, 2)
porcentaje_H4_mas_acotado = round(100*predicciones_con_4_mas_acotado.black_win.sum()/partidas_H4_mas_acotado, 2)
porcentaje_H5_mas_acotado = round(100*predicciones_con_5_mas_acotado.black_win.sum()/partidas_H5_mas_acotado, 2)
porcentaje_H6_mas_acotado = round(100*predicciones_con_6_mas_acotado.black_win.sum()/partidas_H6_mas_acotado, 2)
porcentaje_H7_mas_acotado = round(100*predicciones_con_7_mas_acotado.black_win.sum()/partidas_H7_mas_acotado, 2)
porcentaje_H8_mas_acotado = round(100*predicciones_con_8_mas_acotado.black_win.sum()/partidas_H8_mas_acotado, 2)


porcentajes_mas = [porcentaje_H1_mas, porcentaje_H2_mas, porcentaje_H3_mas, porcentaje_H4_mas,
               porcentaje_H5_mas, porcentaje_H6_mas, porcentaje_H7_mas, porcentaje_H8_mas]
porcentajes_mas_acotado = [porcentaje_H1_mas_acotado, porcentaje_H2_mas_acotado,
                       porcentaje_H3_mas_acotado, porcentaje_H4_mas_acotado,
                       porcentaje_H5_mas_acotado, porcentaje_H6_mas_acotado,
                       porcentaje_H7_mas_acotado, porcentaje_H8_mas_acotado]
heights_mas = [partidas_H1_mas, partidas_H2_mas, partidas_H3_mas, partidas_H4_mas,
               partidas_H5_mas, partidas_H6_mas, partidas_H7_mas, partidas_H8_mas]

heights_mas_acotados = [partidas_H1_mas_acotado, partidas_H2_mas_acotado,
                        partidas_H3_mas_acotado, partidas_H4_mas_acotado,
                        partidas_H5_mas_acotado, partidas_H6_mas_acotado,
                        partidas_H7_mas_acotado, partidas_H8_mas_acotado]


h_leng = len(handicaps_mas)

labels = 'over assigned'
fig = frac_hist_doble(handicaps_mas, porcentajes_mas[:h_leng], porcentajes_mas_acotado[:h_leng], heights_mas[:h_leng],
                      heights_mas_acotados[:h_leng], handicaps_mas, labels, ylim_mas)
fig.savefig(f'./{name}_more.pdf', dpi=100)

############################################################################
################################### handicap de menos  ####################################
############################################################################
# las partidas que si se le dio handicap pero de menos  como salieron
# es decir la diferencia entre los jugadores era para mas handicap que el dado
# partidas con handicap 2, pero deberian haber tenido mas handicap es decir
# deberia perder negro

predicciones_con_1_menos = df_TTT_h[(df_TTT_h.handicap_prediction == 2)
                                    & (df_TTT_h.handicap < 1)]
predicciones_con_2_menos = df_TTT_h[(df_TTT_h.handicap_prediction == 3)
                                    & (df_TTT_h.handicap < 2)]
predicciones_con_3_menos = df_TTT_h[(df_TTT_h.handicap_prediction == 4)
                                    & (df_TTT_h.handicap < 3)]
predicciones_con_4_menos = df_TTT_h[(df_TTT_h.handicap_prediction == 5)
                                    & (df_TTT_h.handicap < 4)]
predicciones_con_5_menos = df_TTT_h[(df_TTT_h.handicap_prediction == 6)
                                    & (df_TTT_h.handicap < 5)]
predicciones_con_6_menos = df_TTT_h[(df_TTT_h.handicap_prediction == 7)
                                    & (df_TTT_h.handicap < 6)]
predicciones_con_7_menos = df_TTT_h[(df_TTT_h.handicap_prediction == 8)
                                    & (df_TTT_h.handicap < 7)]
predicciones_con_8_menos = df_TTT_h[(df_TTT_h.handicap_prediction == 9)
                                    & (df_TTT_h.handicap < 8)]
partidas_H1_menos = predicciones_con_1_menos.shape[0]
partidas_H2_menos = predicciones_con_2_menos.shape[0]
partidas_H3_menos = predicciones_con_3_menos.shape[0]
partidas_H4_menos = predicciones_con_4_menos.shape[0]
partidas_H5_menos = predicciones_con_5_menos.shape[0]
partidas_H6_menos = predicciones_con_6_menos.shape[0]
partidas_H7_menos = predicciones_con_7_menos.shape[0]
partidas_H8_menos = predicciones_con_8_menos.shape[0]
porcentaje_H1_menos = round(100*predicciones_con_1_menos.black_win.sum()/partidas_H1_menos, 2)
porcentaje_H2_menos = round(100*predicciones_con_2_menos.black_win.sum()/partidas_H2_menos, 2)
porcentaje_H3_menos = round(100*predicciones_con_3_menos.black_win.sum()/partidas_H3_menos, 2)
porcentaje_H4_menos = round(100*predicciones_con_4_menos.black_win.sum()/partidas_H4_menos, 2)
porcentaje_H5_menos = round(100*predicciones_con_5_menos.black_win.sum()/partidas_H5_menos, 2)
porcentaje_H6_menos = round(100*predicciones_con_6_menos.black_win.sum()/partidas_H6_menos, 2)
porcentaje_H7_menos = round(100*predicciones_con_7_menos.black_win.sum()/partidas_H7_menos, 2)
porcentaje_H8_menos = round(100*predicciones_con_8_menos.black_win.sum()/partidas_H8_menos, 2)

predicciones_con_1_menos_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 2)
                                                    & (df_TTT_h.handicap == 1)]
predicciones_con_2_menos_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 3)
                                                    & (df_TTT_h.handicap == 2)]
predicciones_con_3_menos_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 4)
                                                    & (df_TTT_h.handicap == 3)]
predicciones_con_4_menos_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 5)
                                                    & (df_TTT_h.handicap == 4)]
predicciones_con_5_menos_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 6)
                                                    & (df_TTT_h.handicap == 5)]
predicciones_con_6_menos_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 7)
                                                    & (df_TTT_h.handicap == 6)]
predicciones_con_7_menos_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 8)
                                                    & (df_TTT_h.handicap == 7)]
predicciones_con_8_menos_acotado = df_TTT_h[(df_TTT_h.handicap_prediction == 9)
                                                    & (df_TTT_h.handicap == 8)]
partidas_H1_menos_acotado = predicciones_con_1_menos_acotado.shape[0]
partidas_H2_menos_acotado = predicciones_con_2_menos_acotado.shape[0]
partidas_H3_menos_acotado = predicciones_con_3_menos_acotado.shape[0]
partidas_H4_menos_acotado = predicciones_con_4_menos_acotado.shape[0]
partidas_H5_menos_acotado = predicciones_con_5_menos_acotado.shape[0]
partidas_H6_menos_acotado = predicciones_con_6_menos_acotado.shape[0]
partidas_H7_menos_acotado = predicciones_con_7_menos_acotado.shape[0]
partidas_H8_menos_acotado = predicciones_con_8_menos_acotado.shape[0]

porcentaje_H1_menos_acotado = round(100*predicciones_con_1_menos_acotado.black_win.sum()/partidas_H1_menos_acotado, 2)
porcentaje_H2_menos_acotado = round(100*predicciones_con_2_menos_acotado.black_win.sum()/partidas_H2_menos_acotado, 2)
porcentaje_H3_menos_acotado = round(100*predicciones_con_3_menos_acotado.black_win.sum()/partidas_H3_menos_acotado, 2)
porcentaje_H4_menos_acotado = round(100*predicciones_con_4_menos_acotado.black_win.sum()/partidas_H4_menos_acotado, 2)
porcentaje_H5_menos_acotado = round(100*predicciones_con_5_menos_acotado.black_win.sum()/partidas_H5_menos_acotado, 2)
porcentaje_H6_menos_acotado = round(100*predicciones_con_6_menos_acotado.black_win.sum()/partidas_H6_menos_acotado, 2)
porcentaje_H7_menos_acotado = round(100*predicciones_con_7_menos_acotado.black_win.sum()/partidas_H7_menos_acotado, 2)
porcentaje_H8_menos_acotado = round(100*predicciones_con_8_menos_acotado.black_win.sum()/partidas_H8_menos_acotado, 2)


h_leng = len(handicaps_menos)
x_ticks = handicaps
porcentajes_menos = [porcentaje_H1_menos, porcentaje_H2_menos, porcentaje_H3_menos, porcentaje_H4_menos,
               porcentaje_H5_menos, porcentaje_H6_menos, porcentaje_H7_menos, porcentaje_H8_menos]
porcentajes_menos_acotado = [porcentaje_H1_menos_acotado, porcentaje_H2_menos_acotado,
                       porcentaje_H3_menos_acotado, porcentaje_H4_menos_acotado,
                       porcentaje_H5_menos_acotado, porcentaje_H6_menos_acotado,
                       porcentaje_H7_menos_acotado, porcentaje_H8_menos_acotado]
heights_menos = [partidas_H1_menos, partidas_H2_menos, partidas_H3_menos, partidas_H4_menos, partidas_H5_menos,
                partidas_H6_menos, partidas_H7_menos, partidas_H8_menos]
heights_menos_acotados = [partidas_H1_menos_acotado, partidas_H2_menos_acotado, partidas_H3_menos_acotado,
                    partidas_H4_menos_acotado, partidas_H5_menos_acotado,
                    partidas_H6_menos_acotado, partidas_H7_menos_acotado, partidas_H8_menos_acotado]


labels = 'under assigned'
fig = frac_hist_doble(handicaps_menos, porcentajes_menos[:h_leng], porcentajes_menos_acotado[:h_leng], heights_menos[:h_leng],
                      heights_menos_acotados[:h_leng],  handicaps_menos, labels, ylim_menos)
fig.savefig(f'./{name}_less.pdf', dpi=100)




print("Sin handicap ")
print("Porcentaje de partidas ganadas por negro")
tot = (predicciones_1.shape[0] + predicciones_2.shape[0] + predicciones_3.shape[0]
      + predicciones_4.shape[0] + predicciones_5.shape[0]
      + predicciones_6.shape[0] + predicciones_7.shape[0])
print("total de partidas consieradas", tot, 'un',
      round(tot*100/total_partidas, 2), '% del total')
print('Sin Handicap:', porcentaje_H1, "% de", partidas_H1, ' Partidas', predicciones_1.proba.mean())
print('Handicap 2:', porcentaje_H2, "% de", partidas_H2, ' Partidas', predicciones_2.proba.mean())
print('Handicap 3:', porcentaje_H3, "% de", partidas_H3, ' Partidas', predicciones_3.proba.mean())
print('Handicap 4:', porcentaje_H4, "% de", partidas_H4, ' Partidas', predicciones_4.proba.mean())
print('Handicap 5:', porcentaje_H5, "% de", partidas_H5, ' Partidas', predicciones_5.proba.mean())
print('Handicap 6:', porcentaje_H6, "% de", partidas_H6, ' Partidas', predicciones_6.proba.mean())
print('Handicap 7:', porcentaje_H7, "% de", partidas_H7, ' Partidas', predicciones_7.proba.mean())
print('Handicap 8:', porcentaje_H8, "% de", partidas_H8, ' Partidas', predicciones_8.proba.mean())
print('Handicap 9:', porcentaje_H9, "% de", partidas_H9, ' Partidas', predicciones_9.proba.mean())

print(" ")
print("Correctas ")
print("Esperamos un equiprobable ya que se dio el handicap que se requeria")
print('Sin Handicap bien:', porcentaje_H1_bien, "% de", partidas_H1_bien, ' Partidas', predicciones_con_1_bien.proba.mean())
print('Con Handicap 2 bien:', porcentaje_H2_bien, "% de", partidas_H2_bien, ' Partidas', predicciones_con_2_bien.proba.mean())
print('Con Handicap 3 bien:', porcentaje_H3_bien, "% de", partidas_H3_bien, ' Partidas', predicciones_con_3_bien.proba.mean())
print('Con Handicap 4 bien:', porcentaje_H4_bien, "% de", partidas_H4_bien, ' Partidas', predicciones_con_4_bien.proba.mean())
print('Con Handicap 5 bien:', porcentaje_H5_bien, "% de", partidas_H5_bien, ' Partidas', predicciones_con_5_bien.proba.mean())
print('Con Handicap 6 bien:', porcentaje_H6_bien, "% de", partidas_H6_bien, ' Partidas', predicciones_con_6_bien.proba.mean())
print('Con Handicap 7 o mas bien:', porcentaje_H7_bien, "% de", partidas_H7_bien, ' Partidas', predicciones_con_7_bien.proba.mean())
print(" ")

print("Color erroneo ")
print("Esperamos un equiprobable ya que se dio el handicap que se requeria")
print('Sin Handicap color:', porcentaje_H1_color, "% de", partidas_H1_color, ' Partidas', predicciones_color_1.proba.mean())
print('Con Handicap 2 color:', porcentaje_H2_color, "% de", partidas_H2_color, ' Partidas', predicciones_color_2.proba.mean())
print('Con Handicap 3 color:', porcentaje_H3_color, "% de", partidas_H3_color, ' Partidas', predicciones_color_3.proba.mean())
print('Con Handicap 4 color:', porcentaje_H4_color, "% de", partidas_H4_color, ' Partidas', predicciones_color_4.proba.mean())
print('Con Handicap 5 color:', porcentaje_H5_color, "% de", partidas_H5_color, ' Partidas', predicciones_color_5.proba.mean())
print('Con Handicap 6 color:', porcentaje_H6_color, "% de", partidas_H6_color, ' Partidas', predicciones_color_6.proba.mean())
print('Con Handicap 7 o mas color:', porcentaje_H7_color, "% de", partidas_H7_color, ' Partidas', predicciones_color_7.proba.mean())
print(" ")


print("De mas ")
print("Esperamos que al haberle dado mas handicap de lo necesario gane mas veces negro, corriendo el equiprobable para arriba")
print('Con Handicap 1 pero requeria menos:', porcentaje_H1_mas_acotado, "% de", partidas_H1_mas_acotado, ' Partidas')# ' No hay partidas con esta condicion')
print('Con Handicap 2 pero requeria menos:', porcentaje_H2_mas_acotado, "% de", partidas_H2_mas_acotado, ' Partidas')# ' No hay partidas con esta condicion')
print('Con Handicap 3 pero requeria menos:', porcentaje_H3_mas_acotado, "% de", partidas_H3_mas_acotado, ' Partidas')
print('Con Handicap 4 pero requeria menos:', porcentaje_H4_mas_acotado, "% de", partidas_H4_mas_acotado, ' Partidas')
print('Con Handicap 5 pero requeria menos:', porcentaje_H5_mas_acotado, "% de", partidas_H5_mas_acotado, ' Partidas')
print('Con Handicap 6 pero requeria menos:', porcentaje_H6_mas_acotado, "% de", partidas_H6_mas_acotado, ' Partidas')
print(" ")
print("De menos ")
print("Esperamos que al necesitar mas handicap gane mas veces blanco, corriendo el equiprobable para abajo")
print('Con Handicap 2 pero requeria mas:', porcentaje_H2_menos_acotado, "% de", partidas_H2_menos_acotado, ' Partidas')
print('Con Handicap 3 pero requeria mas:', porcentaje_H3_menos_acotado, "% de", partidas_H3_menos_acotado, ' Partidas')
print('Con Handicap 4 pero requeria mas:', porcentaje_H4_menos_acotado, "% de", partidas_H4_menos_acotado, ' Partidas')
print('Con Handicap 5 pero requeria mas:', porcentaje_H5_menos_acotado, "% de", partidas_H5_menos_acotado, ' Partidas')
print('Con Handicap 6 pero requeria mas:', porcentaje_H6_menos_acotado, "% de", partidas_H6_menos_acotado, ' Partidas')
print(" ")



'''
############################################################################
###################################   porcentajes    ####################################
############################################################################
partidas_H_estimadas_total = df_TTT_h[df_TTT_h.handicap_prediction >= 2].shape[0]

partidas_H_estimadas_reales = df_TTT_h[(df_TTT_h.handicap_prediction >= 2) & (df_TTT_h.handicap > 1)].shape[0]
wins_predichos = round(df_TTT_h.black_win[(df_TTT_h.handicap_prediction >= 2)
                       & (df_TTT_h.handicap == 1)].sum(), 4)
partidas_wins_predichos = df_TTT_h.black_win[(df_TTT_h.handicap_prediction >= 2)
                                             & (df_TTT_h.handicap == 0)].shape[0]
print(" ")

print("Numero de partidas con Handicap real: ", partidas_H, f'= {round(partidas_H*100/total_partidas, 4)}', '%')
print("Numero de partidas con Handicap estimado: ", partidas_H_estimadas_total,
      f'= {round(partidas_H_estimadas_total*100/total_partidas,1)}%')
print("Numero de partidas que coinciden: ", partidas_H_estimadas_reales,
      f'= {round(partidas_H_estimadas_reales*100/partidas_H,1)}%',
      'del total de partidas con handicap')
print("Numero de partidas sin handicap pero que deberian tener: ",
      partidas_wins_predichos, f'= {round(partidas_wins_predichos*100/total_partidas,1)}%')
print("Numero de partidas ganadas, las cuales no tenian handicap pero estiamos que deberian: ",
      wins_predichos, f'= {round(wins_predichos*100/partidas_wins_predichos,1)}%',
      'del total de partidas sin handicap pero que deberian tener')

print(" ")
predichos_negativos = df_TTT_h[df_TTT_h.mean_Diff <= h_value].shape[0]
# Sumo la cantidad de unos que tiene black_win, es decir la cantidad de partidas ganadas por negro.
wins_predichos_negativos = round(df_TTT_h.black_win[df_TTT_h.mean_Diff <= h_value].sum(), 4)
wins_predichos_negativos_H = round(df_TTT_h.black_win[(df_TTT_h.mean_Diff <= h_value)&(df_TTT_h.handicap>0)].sum(), 4)
predichos_negativos_conH_mal = df_TTT_h[(df_TTT_h.mean_Diff <= h_value) &
                                        (df_TTT_h.handicap >= 2)].shape[0]

print("Numero de partidas con asignacion de color contraria estimada: ", predichos_negativos,
      f' = {round(predichos_negativos*100/total_partidas,1)}%', 'del total de partidas ')
print('Numero de partidas perdidas: ', wins_predichos_negativos,
      f' = {round(wins_predichos_negativos*100/predichos_negativos,1)}%', f'del total de partidas con mala asignacion de color.')
print("Numero de partidas con asignacion contraria y mal asignacion de handicap",
      predichos_negativos_conH_mal, f' = {round(predichos_negativos_conH_mal*100/predichos_negativos,1)}%',
      f'del total de partidas con mala asignacion de color.  De estas {wins_predichos_negativos_H} = {round(wins_predichos_negativos_H*100/predichos_negativos_conH_mal,1)} perdieron')

'''
################################################################################
######################### ESTIMACIONES GANADAS #################################
################################################################################
'''
df_TTT_h.loc[:,'Diff_ganador'] = df_TTT_h.black_win.apply(lambda x: 1 if x>=h_value else 0)
df_TTT_h.loc[:,'winner'] = df_TTT_h.apply(lambda x:  x['b_mean'] if x['black_win']==1 else x['w_mean'], axis=1)
df_TTT_h.loc[:,'looser'] = df_TTT_h.apply(lambda x:  x['b_mean'] if x['black_win']==0 else x['w_mean'], axis=1)
df_ts_h.loc[:,'winner'] = df_ts_h.apply(lambda x:  x['b_mean'] if x['black_win']==1 else x['w_mean'], axis=1)
df_ts_h.loc[:,'looser'] = df_ts_h.apply(lambda x:  x['b_mean'] if x['black_win']==0 else x['w_mean'], axis=1)

df_TTT_h['winner_Diff'] = df_TTT_h['winner'] - df_TTT_h['looser']
wins_predicts = df_TTT_h[df_TTT_h.winner_Diff > 0].shape[0]
df_ts_h['winner_Diff'] = df_ts_h['winner'] - df_TTT_h['looser']
wins_predicts_ts = df_ts_h[df_ts_h.winner_Diff > 0].shape[0]
print('Total de partidas: ', df_TTT_h.shape[0], ' | Predichas: ', wins_predicts, ' = ', round(wins_predicts*100/df_TTT_h.shape[0],1) ,'%')
print('Total de partidas: ', df_ts_h.shape[0], ' | Predichas_ts: ', wins_predicts_ts, ' = ', round(wins_predicts_ts*100/df_ts_h.shape[0],1) ,'%')
'''
