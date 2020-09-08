import sys
sys.path.append("../../paquetes/trueskill/")
import pandas as pd
import src as ttt
from importlib import reload

reload(ttt)

from collections import defaultdict
df = pd.read_csv('./simulacion.csv')
df = df[:2500]
#prior_dict = defaultdict(lambda:env.Rating(0,25/3,0,1/100))
#for h_key in set([(h,s) for h, s in zip(df.handicap, df.width) ]):
#    prior_dict[h_key]
#dict(prior_dict)

results = list(df.black_win.map(lambda x: [0,1] if x else [1,0]))
composition = [[[str(w)], [str(b)]] for w, b in zip(df.white, df.black)]
batch = range(0, len(results))
h = ttt.History(composition, results, batch)
#history.trueSkill()
h.convergence()
w_mean = [print(w) for t,w,b in zip(h.times,df.white,df.black) ]

w_mean = [ h.batches[t].posterior(w).mu for t,w,b in zip(h.times,df.white,df.black) ]
b_mean = [ h.batches[t].posterior(b).mu for t,w,b in zip(h.times,df.white,df.black) ]
w_std = [ h.batches[t].posterior(w).sigma for t,w,b in zip(h.times,df.white,df.black) ]
b_std = [ h.batches[t].posterior(b).sigma for t,w,b in zip(h.times,df.white,df.black) ]
evidence = [  h.batches[t].evidences[0] for t in h.times]

res = df.copy()
res["w_mean"] = w_mean
res["w_std"] = w_std
res["b_mean"] = b_mean
res["b_std"] = b_std
res["evidence"] = evidence


res.to_csv("TTT_python.csv", index=False)
