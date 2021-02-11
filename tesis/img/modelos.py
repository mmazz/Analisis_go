import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df_TTT_h = pd.read_csv('./rela_beta_sigma_zoom.csv')
def compute_model_posterior(log_ev):
    le = np.array(log_ev) # lista de [log p(D|M_i)] vectorizada
    lp = np.log(1/len(log_ev)) # log p(M_i), mismo para todos los modelos
    propotional_log_posterior = le + lp #  log p(D|M) + log P(M)  el posterior proporcional
    print(propotional_log_posterior)
    c  = np.max(le + lp) # Constante
    propotional_log_posterior = propotional_log_posterior  - c #
    print(propotional_log_posterior)
    model_posterior = np.exp(propotional_log_posterior)/sum(np.exp(propotional_log_posterior))
    print(np.exp(propotional_log_posterior))
    print(sum(np.exp(propotional_log_posterior)))
    return model_posterior

list = [round(df_TTT_h["tres_beta_ttt"][5],2),round(df_TTT_h["tres_beta_ts"][5],2) ]
list2 = [0.652*-1600000, 0.649*-1600000]

print(compute_model_posterior(list2))
