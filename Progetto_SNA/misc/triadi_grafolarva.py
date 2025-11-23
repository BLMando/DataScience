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


# %%
def remove_duplicate_tuples(tuples_list):
    unique_tuples_set = set()

    for tpl in tuples_list:
        sorted_tpl = tuple(sorted(tpl))
        unique_tuples_set.add(sorted_tpl)

    # Convert the set back to a list of tuples if needed
    unique_tuples_list = list(unique_tuples_set)
    return unique_tuples_list


# %% [markdown]
# # Larva

# %%
connectivity_matrix = pd.read_csv("../data/all-all_connectivity_matrix.csv", header=[0], index_col=[0])
connectivity_matrix = connectivity_matrix.map(lambda x: 1 if x != 0 else 0)

# %%
g = ig.Graph.Adjacency(connectivity_matrix, mode='directed')

nodes = g.vs.indices

edges = g.get_edgelist()
edges_set = set(edges)

# %%
#tc = g.triad_census()

#with open('triadi_larva/triad_census.pkl', 'wb') as f:
#            pickle.dump(tc, f) 

with open('triadi_larva/triad_census.pkl', 'rb') as file:
            tc = pickle.load(file)

# %%
tc.t300

# %%
ba_bc = [] #021D
ab_cb = [] #021U
ab_bc = [] #021C
ab_ba_cb = [] #111D
ab_bc_ba = [] #111U
ab_cb_ac = [] #030T
ba_cb_ac = [] #030C
ab_ba_ac_ca = [] #201
ba_bc_ca_ac = [] #120D
ab_cb_ac_ca = [] #120U
ab_bc_ca_ac = [] #120C
ab_bc_cb_ca_ac = [] #210
ab_ba_ac_ca_bc_cb = [] #300

# %%
for a in nodes:
    
    neighbor_vertices_a = g.vs[g.neighbors(a, mode="all")]
    neighbor_ids_a = [vertex.index for vertex in neighbor_vertices_a]
    
    for b in neighbor_ids_a:
        
        neighbor_vertices_b = g.vs[g.neighbors(b, mode="all")]
        neighbor_ids_b = [vertex.index for vertex in neighbor_vertices_b]
        
        union_neighbor_ab = list(set().union(neighbor_ids_a, neighbor_ids_b))    

        while a in union_neighbor_ab: union_neighbor_ab.remove(a)
        while b in union_neighbor_ab: union_neighbor_ab.remove(b)

        for c in union_neighbor_ab:

            # 021D ba_bc
            if (b, a) in edges_set and (b, c) in edges_set and (a, b) not in edges_set and (a, c) not in edges_set and (c, b) not in edges_set and (c, a) not in edges_set:
                if (a, b) not in edges_set and (c, b) not in edges_set:
                    ba_bc.append((a, b, c))

            # 021U ab_cb
            if (a, b) in edges_set and (c, b) in edges_set and (b, a) not in edges_set and (b, c) not in edges_set and (a, c) not in edges_set and (c, a) not in edges_set:
                    ab_cb.append((a, b, c))

            # 021C ab_bc
            if (a, b) in edges_set and (b, c) in edges_set and (b, a) not in edges_set and (c, b) not in edges_set and (a, c) not in edges_set and (c, a) not in edges_set:
                ab_bc.append((a, b, c))

            # 111D ab_ba_cb
            if (a, b) in edges_set and (b, a) in edges_set and (c, b) in edges_set and (b, c) not in edges_set and (a, c) not in edges_set and (c, a) not in edges_set:
                ab_ba_cb.append((a, b, c))

            # 111U ab_bc_ba
            if (a, b) in edges_set and (b, c) in edges_set and (b, a) in edges_set and (c, b) not in edges_set and (a, c) not in edges_set and (c, a) not in edges_set:
                ab_bc_ba.append((a, b, c))

            # 030T ab_cb_ac
            if (a, b) in edges_set and (c, b) in edges_set and (a, c) in edges_set and (b, a) not in edges_set and (b, c) not in edges_set and (c, a) not in edges_set:
                ab_cb_ac.append((a, b, c))

            # 030C ba_cb_ac
            if (b, a) in edges_set and (c, b) in edges_set and (a, c) in edges_set and (a, b) not in edges_set and (b, c) not in edges_set and (c, a) not in edges_set:
                ba_cb_ac.append((a, b, c))

            # 201 ab_ba_ac_ca
            if (a, b) in edges_set and (b, a) in edges_set and (a, c) in edges_set and (c, a) in edges_set and (b, c) not in edges_set and (c, b) not in edges_set:
                ab_ba_ac_ca.append((a, b, c))

            # 120D ba_bc_ca_ac
            if (b, a) in edges_set and (b, c) in edges_set and (c, a) in edges_set and (a, c) in edges_set and (a, b) not in edges_set and (c, b) not in edges_set:
                ba_bc_ca_ac.append((a, b, c))

            # 120U ab_cb_ac_ca
            if (a, b) in edges_set and (c, b) in edges_set and (a, c) in edges_set and (c, a) in edges_set and (b, a) not in edges_set and (b, c) not in edges_set:
                ab_cb_ac_ca.append((a, b, c))

            # 120C ab_bc_ca_ac
            if (a, b) in edges_set and (b, c) in edges_set and (c, a) in edges_set and (a, c) in edges_set and (b, a) not in edges_set and (c, b) not in edges_set:
                ab_bc_ca_ac.append((a, b, c))

            # 210 ab_bc_cb_ca_ac
            if (a, b) in edges_set and (b, c) in edges_set and (c, b) in edges_set and (c, a) in edges_set and (a, c) in edges_set and (b, a) not in edges_set:
                ab_bc_cb_ca_ac.append((a, b, c))


# %%
with open('triadi_larva/021D.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ba_bc), f) #021D

with open('triadi_larva/021U.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ab_cb), f) #021U

with open('triadi_larva/021C.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ab_bc), f)

with open('triadi_larva/111D.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ab_ba_cb), f)

with open('triadi_larva/111U.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ab_bc_ba), f) 

with open('triadi_larva/030T.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ab_cb_ac), f) 

with open('triadi_larva/030C.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ba_cb_ac), f) 

with open('triadi_larva/201.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ab_ba_ac_ca), f) 

with open('triadi_larva/120D.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ba_bc_ca_ac), f)

with open('triadi_larva/120U.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ab_cb_ac_ca), f)

with open('triadi_larva/120C.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ab_bc_ca_ac), f)

with open('triadi_larva/210.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ab_bc_cb_ca_ac), f)

# %%
ab_ba_ac_ca_bc_cb = []

already_visited = []

for a in nodes:
    
    neighbor_vertices_a = g.vs[g.neighbors(a, mode="all")]
    neighbor_ids_a = [vertex.index for vertex in neighbor_vertices_a]
    already_visited.append(a)
    
    for b in neighbor_ids_a:

        if b in already_visited:
                continue
        
        neighbor_vertices_b = g.vs[g.neighbors(b, mode="all")]
        neighbor_ids_b = [vertex.index for vertex in neighbor_vertices_b]
        
        union_neighbor_ab = list(set().union(neighbor_ids_a, neighbor_ids_b))    

        while a in union_neighbor_ab: union_neighbor_ab.remove(a)
        while b in union_neighbor_ab: union_neighbor_ab.remove(b)
        
        for c in union_neighbor_ab:
            if c in already_visited:
                continue
                
            # 300 ab_ba_ac_ca_bc_cb
            if (a, b) in edges_set and (b, a) in edges_set and (a, c) in edges_set and (c, a) in edges_set and (b, c) in edges_set and (c, b) in edges_set:
                ab_ba_ac_ca_bc_cb.append((a, b, c))

# %%
with open('triadi_larva/300.pkl', 'wb') as f:
            pickle.dump(remove_duplicate_tuples(ab_ba_ac_ca_bc_cb), f)

# %%
print('igraph: ' + str(tc.t021d) + ' nostro: ' + str(len(set(ba_bc)))) #021D
print('igraph: ' + str(tc.t021u) + ' nostro: ' + str(len(set(ab_cb)))) #021U
print('igraph: ' + str(tc.t021c) + ' nostro: ' + str(len(set(ab_bc)))) #021C
print('igraph: ' + str(tc.t111d) + ' nostro: ' + str(len(set(ab_ba_cb)))) #111D
print('igraph: ' + str(tc.t111u) + ' nostro: ' + str(len(set(ab_bc_ba)))) #111U
print('igraph: ' + str(tc.t030t) + ' nostro: ' + str(len(set(ab_cb_ac)))) #030T
print('igraph: ' + str(tc.t030c) + ' nostro: ' + str(len(set(ba_cb_ac)))) #030C
print('igraph: ' + str(tc.t201) + ' nostro: ' + str(len(set(ab_ba_ac_ca)))) #201
print('igraph: ' + str(tc.t120d) + ' nostro: ' + str(len(set(ba_bc_ca_ac)))) #120D
print('igraph: ' + str(tc.t120u) + ' nostro: ' + str(len(set(ab_cb_ac_ca)))) #120U
print('igraph: ' + str(tc.t120c) + ' nostro: ' + str(len(set(ab_bc_ca_ac)))) #120C
print('igraph: ' + str(tc.t210) + ' nostro: ' + str(len(set(ab_bc_cb_ca_ac)))) #210
print('igraph: ' + str(tc.t300) + ' nostro: ' + str(len(set(ab_ba_ac_ca_bc_cb)))) #300

# %%
print('021D igraph: ' + str(tc.t021d) + ' nostro: ' + str(len(remove_duplicate_tuples(ba_bc)))) #021D
print('021U igraph: ' + str(tc.t021u) + ' nostro: ' + str(len(remove_duplicate_tuples(ab_cb)))) #021U
print('021C igraph: ' + str(tc.t021c) + ' nostro: ' + str(len(remove_duplicate_tuples(ab_bc)))) #021C
print('111D igraph: ' + str(tc.t111d) + ' nostro: ' + str(len(remove_duplicate_tuples(ab_ba_cb)))) #111D
print('111U igraph: ' + str(tc.t111u) + ' nostro: ' + str(len(remove_duplicate_tuples(ab_bc_ba)))) #111U
print('030T igraph: ' + str(tc.t030t) + ' nostro: ' + str(len(remove_duplicate_tuples(ab_cb_ac)))) #030T
print('030C igraph: ' + str(tc.t030c) + ' nostro: ' + str(len(remove_duplicate_tuples(ba_cb_ac)))) #030C
print('201 igraph: ' + str(tc.t201) + ' nostro: ' + str(len(remove_duplicate_tuples(ab_ba_ac_ca)))) #201
print('120D igraph: ' + str(tc.t120d) + ' nostro: ' + str(len(remove_duplicate_tuples(ba_bc_ca_ac)))) #120D
print('120U igraph: ' + str(tc.t120u) + ' nostro: ' + str(len(remove_duplicate_tuples(ab_cb_ac_ca)))) #120U
print('120C igraph: ' + str(tc.t120c) + ' nostro: ' + str(len(remove_duplicate_tuples(ab_bc_ca_ac)))) #120C
print('210 igraph: ' + str(tc.t210) + ' nostro: ' + str(len(remove_duplicate_tuples(ab_bc_cb_ca_ac)))) #210
print('300 igraph: ' + str(tc.t300) + ' nostro: ' + str(len(remove_duplicate_tuples(ab_ba_ac_ca_bc_cb)))) #300

# %%
