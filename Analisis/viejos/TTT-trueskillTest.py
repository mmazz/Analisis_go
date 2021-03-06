import sys
sys.path.append('/home/mati/Storage/Tesis/AnalisisGo-Tesis/trueskill')
import pandas as pd
import TTT as th
from importlib import reload

reload(th)
path = '/home/mati/Storage/Tesis/AnalisisGo-Tesis/Example2.csv'
df = pd.read_csv(path)
env = th.TrueSkill()
player = {}
ptrueskill = {}

# Can define an other Prior
globalPrior = env.Rating(mu=25, sigma=25/3, beta=25/6)
for i in df.index:
    p1_key = str(df.loc[i].Player1)
    p2_key = str(df.loc[i].Player2)
    prior_1 = player.get(p1_key, globalPrior)
    prior_2 = player.get(p2_key, globalPrior)
    t1 = [prior_1.forget(1)]  # add noise to prior
    t2 = [prior_2.forget(1)]
    result = [1, 0] if df.loc[i].Result=='[1, 0]' else [0, 1]
    game = env.Game([t1, t2], result)
    t1_post, t2_post = game.posterior
    player[p1_key] = t1_post[0]
    player[p2_key] = t2_post[0]

print(player)
#%%
composition = [[[p1], [p2]] for p1, p2 in zip(df.Player1, df.Player2)]
results = list(df.Result.map(lambda x: [1, 0] if x=='[1, 0]' else [0, 1]))
history = env.history(composition, results)
history.trueskill()
print(history.posteriors_player())
