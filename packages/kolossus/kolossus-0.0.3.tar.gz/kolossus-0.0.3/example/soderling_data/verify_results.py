
import numpy as np
import pandas as pd


df = pd.read_csv('human_kinase_substrate_predictions.csv', nrows=500)
df['seqid'] = [f'seq{i+1}' for i in range(len(df))]
df = pd.melt(df, ['Substrate', 'seqid'], var_name='kinase', value_name='prob')

import re 
query = r'^seq[0-9]+$'
#query = 'boogaloo'
def fix(s):
    return f'{s}:psite=7' if re.search(query, s) else s
d1 = dict(map(lambda t: ((t[0], fix(t[1])), t[2]), df[['kinase', 'seqid', 'prob']].values.tolist()))

with open('results.txt', 'rt') as f:
    lines = [line.strip().split() for line in f.readlines() if not line.startswith('#')]

d2 = dict(map(lambda t: ((t[0], t[1]), float(t[2])), lines))

a = []
for k in d2:
    a.append(abs(d1[k] - d2[k]) < 1e-4)

print(all(a))

def cos_sim(x, y):
    return np.dot(x, y) / (np.sqrt(x@x) * np.sqrt(y@y))

import h5py 
with h5py.File('results.h5', 'r') as f1, open('results.txt') as f2:
    pp = []
    cc = []
    for line in f2:
        if line.strip().startswith('#'):
            continue
        k1, k2, p = line.split()
        pp.append(float(p))
        cc.append(cos_sim(f1[k1][:], f1[k2][:]))
print(np.allclose(*list(map(np.array, [pp, cc]))))
