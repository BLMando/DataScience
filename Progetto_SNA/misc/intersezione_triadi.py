# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import igraph as ig
import pickle
import itertools
import timeit
import datetime

# %% [markdown]
# ## Larva

# %%
_120D = [] #ba_bc_ca_ac
_120U = [] #ab_cb_ac_ca
_120C = [] #ab_bc_ca_ac
_210 = [] #ab_bc_cb_ca_ac
_300 = [] #ab_ba_ac_ca_bc_cb

# %%
with open('triadi_larva/120D.pkl', 'rb') as f:
    _120D = pickle.load(f)

with open('triadi_larva/120U.pkl', 'rb') as f:
    _120U = pickle.load(f)

with open('triadi_larva/120C.pkl', 'rb') as f:
    _120C = pickle.load(f)

with open('triadi_larva/210.pkl', 'rb') as f:
    _210 = pickle.load(f)

with open('triadi_larva/300.pkl', 'rb') as f:
    _300 = pickle.load(f)

# %%
len(_120D)

# %%
len(_120U)

# %%
len(_120C)

# %%
len(_210)

# %%
len(_300)

# %%
_120D_120U = [] 
_120D_120C = [] 
_120D_210 = [] 
_120D_300 = [] 

_120U_120C = [] 
_120U_210 = [] 
_120U_300 = [] 

_120C_210 = [] 
_120C_300 = [] 

_210_300 = []  

# %%
i = 0
print('Time: ', str(datetime.datetime.now()))  

for t1 in _120D:
    t1 = set(t1)

    for t2 in _120U:
        t2 = set(t2)
        common = t1.intersection(t2)
        if len(common) >=2:
            _120D_120U.append([t1, t2, common])
            
    for t2 in _120C:
        t2 = set(t2)
        common = t1.intersection(t2)
        if len(common) >=2:
            _120D_120C.append([t1, t2, common])

    for t2 in _210:
        t2 = set(t2)
        common = t1.intersection(t2)
        if len(common) >=2:
            _120D_210.append([t1, t2, common])
            
    for t2 in _300:
        t2 = set(t2)
        common = t1.intersection(t2)
        if len(common) >=2:
            _120D_300.append([t1, t2, common])

    if i % 500 == 0:
        print(i)
        print('Time: ', str(datetime.datetime.now()))  
            
    i = i+1

# %%
i = 0
print('Time: ', str(datetime.datetime.now()))  

for t1 in _120U: 
    t1 = set(t1)
    
    for t2 in _120C:
        t2 = set(t2)
        common = t1.intersection(t2)
        if len(common) >=2:
            _120U_120C.append([t1, t2, common])

    for t2 in _210:
        t2 = set(t2)
        common = t1.intersection(t2)
        if len(common) >=2:
            _120U_210.append([t1, t2, common])
            
    for t2 in _300:
        t2 = set(t2)
        common = t1.intersection(t2)
        if len(common) >=2:
            _120U_300.append([t1, t2, common])

    if i % 1000 == 0:
        print(i)
        print('Time: ', str(datetime.datetime.now()))  
            
    i = i+1

# %%
i = 0
print('Time: ', str(datetime.datetime.now()))  

for t1 in _120C: 
    t1 = set(t1)
    
    for t2 in _210:
        t2 = set(t2)
        common = t1.intersection(t2)
        if len(common) >=2:
            _120C_210.append([t1, t2, common])
            
    for t2 in _300:
        t1 = set(t1)
        t2 = set(t2)
        common = t1.intersection(t2)
        if len(common) >=2:
            _120C_300.append([t1, t2, common])

    if i % 2000 == 0:
        print(i)
        print('Time: ', str(datetime.datetime.now()))  
            
    i = i+1

# %%
i = 0
print('Time: ', str(datetime.datetime.now()))  

for t1 in _120C:
    t1 = set(t1)
    
    for t2 in _300:
        t2 = set(t2)
        common = t1.intersection(t2)
        if len(common) >=2:
            _120C_300.append([t1, t2, common])

    if i % 5000 == 0:
        print(i)
        print('Time: ', str(datetime.datetime.now()))  
            
    i = i+1

# %%
with open('triadi_larva/_120D_120C.pkl', 'rb') as f:
    _120D_120C = pickle.load(f)

print(len(_120D_120C))

print(len(set([str(sorted(x)) for x in _120D_120C])))

# %%
with open('triadi_larva/_120D_120U.pkl', 'rb') as f:
    _120D_120U = pickle.load(f)

print(len(_120D_120U))

print(len(set([str(sorted(x)) for x in _120D_120U])))

# %%
with open('triadi_larva/_120D_210.pkl', 'rb') as f:
    _120D_210 = pickle.load(f)

print(len(_120D_210))

print(len(set([str(sorted(x)) for x in _120D_210])))

# %%
with open('triadi_larva/_120D_300.pkl', 'rb') as f:
    _120D_300 = pickle.load(f)

print(len(_120D_300))

print(len(set([str(sorted(x)) for x in _120D_300])))

# %% [markdown]
# ## Intersezione di 300 con sé stesso

# %%
_300_300 = []

i = 0
print('Time: ', str(datetime.datetime.now()))  

for t1 in _300:
    t1 = set(t1)

    for t2 in _300:
        t2 = set(t2) 
        if(t1!=t2):
            if len(t1.intersection(t2)) >=2:
                _300_300.append([t1, t2, t1.intersection(t2), t1^t1])

    if i % 5000 == 0:
        print(i)
        print('Time: ', str(datetime.datetime.now()))  
            
    i = i+1

with open('triadi_larva/300_300.pkl', 'wb') as f:
            pickle.dump(_300_300, f) 

# %%
len(_300_300)

# %%
len(_300_300)

# %%
df = pd.DataFrame(_300_300, columns=('t1', 't2', 'intersection'))

df['intersection'] = df['intersection'].apply(lambda x: sorted(x)).astype(str)

# %%
df['count'] = 1
# print(df.groupby(['intersection'])['count'].sum().to_string())
df.groupby(['intersection'])['count'].sum()

# %% [markdown]
# ## Clique di dimensione 4

# %% [markdown]
# motif = sono cose che compaiono molte volte. Trovare struttura che si ripetono molte volte
#
# Solo triadi 300 al momento. So che sono molto freuqenti. NOn ci posso ragionare ancora. 
#
# Quello che possiamo vedere è quante sono le clique di dimensione 4 totalmente connesse, poi 5, poi 6.
# traidi/clique
#
# Comincio a individuare tutte le clique complete di dimensione 3, poi 4, poi 5 e vediamo cosa otteniamo, cioè ogni volta di quanto si riduce la frequenza.
#
# Quelle iperfrequenti non sono path. A me serve una struttura né troppo né troppo poca.
#
# Quello che stiamo facendo è una sorta di apriori, ma non mi voglio fermare alle clique, ma poi voglio andare anche alle quasi clique quindi anche considerando ad esempio quello che succede quando manca un arco. 

# %%
with open('triadi_larva/300_300.pkl', 'rb') as f:
    _300_300 = pickle.load(f)

# %%
connectivity_matrix = pd.read_csv("../data/all-all_connectivity_matrix.csv", header=[0], index_col=[0])
connectivity_matrix = connectivity_matrix.map(lambda x: 1 if x != 0 else 0)

g = ig.Graph.Adjacency(connectivity_matrix, mode='directed')

nodes = g.vs.indices

edges = g.get_edgelist()
edges_set = set(edges)

# %%
triads_intersection = pd.DataFrame(_300_300, columns=('t1', 't2', 'intersection', 'difference'))

# %%
triads_intersection

# %%
cliques_4 = []

i = 0
print('Time: ', str(datetime.datetime.now()))  

for index, row in triads_intersection.iterrows():
    difference = list(row['difference'])
    t1 = list(row['t1'])
    t2 = list(row['t2'])
    
    if (difference[0], difference[1]) in edges_set and (difference[1], difference[0]) in edges_set:
        if sorted(list(set(t1)|set(t2))) not in cliques_4:
            cliques_4.append(sorted(list(set(t1)|set(t2))))

    if i % 300000 == 0:
        print(i)
        print('Time: ', str(datetime.datetime.now()))  
            
    i = i+1


# %%
with open('triadi_larva/cliques_4.pkl', 'wb') as f:
            pickle.dump(cliques_4, f)

# %%
len(cliques_4)

# %%
len(set([str(x) for x in cliques_4]))

# %%
len(cliques_4)

# %% [markdown]
# ## Clique di dimensione 5

# %%
cliques4_300 = []

i = 0
print('Time: ', str(datetime.datetime.now()))  

for clique in cliques_4:
    clique = set(clique)

    for t in _300:
        t = set(t) 
        if len(clique.intersection(t)) == 2:
           cliques4_300.append([clique, t, clique.intersection(t), clique^t])

    if i % 5000 == 0:
        print(i)
        print('Time: ', str(datetime.datetime.now()))  
            
    i = i+1

with open('triadi_larva/cliques4_300.pkl', 'wb') as f:
            pickle.dump(cliques4_300, f) 

# %%
with open('triadi_larva/cliques4_300.pkl', 'rb') as f:
    cliques4_300 = pickle.load(f)

# %%
cliques4_300_intersection = pd.DataFrame(cliques4_300, columns=('clique', 'triad', 'intersection', 'difference'))

# %%
cliques_5 = []

i = 0
print('Time: ', str(datetime.datetime.now()))  

for index, row in cliques4_300_intersection.iterrows():
    intersection = list(row['intersection'])
    difference = list(row['difference'])
    clique_nodes = list(set(row['clique']) - set(intersection))
    triad_node = list(set(row['triad']) - set(intersection))[0] 

    nodes_5 = sorted(intersection + difference)

    if (clique_nodes[0], triad_node) in edges_set and (clique_nodes[1], triad_node) in edges_set and (triad_node, clique_nodes[0]) in edges_set and (triad_node, clique_nodes[1]) in edges_set:
        cliques_5.append(nodes_5)

    if i % 300000 == 0:
        print(i)
        print('Time: ', str(datetime.datetime.now()))  
            
    i = i+1

with open('triadi_larva/cliques_5.pkl', 'wb') as f:
            pickle.dump(cliques_5, f)

# %%
len(set([str(x) for x in cliques_5]))

# %%
