import sys
sys.path.append('./')
import pandas as pd
import trueskill as th
from importlib import reload

reload(th)
path = './simulacion.csv'
df = pd.read_csv(path)
env = th.TrueSkill(mu=25.0, sigma=25/3, beta=25/6, tau=0.5, draw_probability=0.0, )
player = {}
ptrueskill = {}

# Can define an other Prior
globalPrior = env.Rating(mu=25, sigma=25/3)
for i in df.index:
    p1_key = str(df.loc[i].white)
    p2_key = str(df.loc[i].black)
    prior_1 = player.get(p1_key, globalPrior)
    prior_2 = player.get(p2_key, globalPrior)
    t1 = [prior_1]  # add noise to prior
    t2 = [prior_2]
    result = [1, 0] if df.loc[i].black_win == 0 else [0, 1]
    t1_post, t2_post = env.rate([t1, t2], result)
    player[p1_key] = t1_post[0]
    player[p2_key] = t2_post[0]

print(player)
#%%
