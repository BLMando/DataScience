# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
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

# %% [markdown]
# # Analisi della social network tra istituti di ricerca e università.
# L'obiettivo di questa analisi è quella di individuare se, all'interno della comunità scientifica, esistano
# dei gruppi naturali (comunità) tra i diversi istituti di ricerca nel campo della Energia.
# %%
from importlib import reload
from datetime import datetime
from pathlib import Path
from tqdm.notebook import tqdm
from importlib import reload  # Python 3.4+
import utils.graphing as graphing
import utils.metrics as metrics
import networkx as nx
import os
from time import sleep
import pandas as pd
import utils.preproc as preproc
import warnings
import math
import numpy as np


CITATIONS_DIRECTED_GRAPH = "./data/cit-HepTG.txt"
CITATIONS_ABSTRACTS_DIR = "./data/cit-HepTh-abstracts"

ROR_DATA = "./data/ror-data.csv"
UNIVERSITIES_DATA = "./data/all_universities.csv"

warnings.filterwarnings("ignore")

# %% [markdown]
# ## nuova sessione
# Questa linea genera la session_id.
# Se la sovrascrivi si intende che hai fatto cambiamenti al dataset perciò il resto del codice non farà più affidamento alla sessione precedente e quindi alcuni file
# vanno rigenerati
# %% jupyter={"source_hidden": true}
s = datetime.now().strftime("%y%m%d%H%M")
session_id = f"{s}"  # NUOVA SESSIONE
SESSION_PATH = f"data/sessions/{session_id}"
os.makedirs(SESSION_PATH, exist_ok=True)

# %% [markdown]
# ## caricamento sessione
# %% jupyter={"source_hidden": true}
session_id = "2511212247"  # RICARICA UNA SESSIONE
SESSION_PATH = f"data/sessions/{session_id}"

# %% jupyter={"source_hidden": true}
citations_uni = pd.read_csv(f"{SESSION_PATH}/citations-uni.csv")
citations_country = pd.read_csv(f"{SESSION_PATH}/citations-country.csv")
papers = pd.read_csv(f"{SESSION_PATH}/papers.csv")

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# # Preprocessamento
# eseguiamo le operazioni preliminari di caricamento dei dati
#
# citations contiene il grafo diretto con colonne target e source
# %%
records = []

for abp in tqdm(Path(CITATIONS_ABSTRACTS_DIR).rglob("*")):
    if abp.is_file():
        with open(abp, "r", encoding="utf-8", errors="ignore") as f:
            abs = f.read()

        data = {"id": abp.stem}
        fields = preproc.extract_fields(abs)
        # preproc è una classe statica definita in utils.py

        if isinstance(fields, dict):
            data.update(fields)
            records.append(data)

papers = pd.DataFrame(records)
del records

# %%
ror

# %% jupyter={"source_hidden": true}
universities

# %% [markdown]
# Mapping dei paper alle rispettive università
# %%
ror = pd.read_csv(ROR_DATA)
ror["clean_url"] = (
    ror["links"].str.replace(r"^https?://", "", regex=True).str.split("/").str[0]
)
ror["tld2"] = ror["clean_url"].str.extract(r"([a-zA-Z0-9-]+\.[a-zA-Z0-9-]+)$")

universities = pd.read_csv(UNIVERSITIES_DATA)

# %% jupyter={"source_hidden": true}
ror

# %% jupyter={"source_hidden": true}
domain_mapping = {
    str(row.id): preproc.extract_domain(row.email, ror, universities)
    for row in tqdm(papers.itertuples())
}

# %% jupyter={"source_hidden": true}

# %% jupyter={"source_hidden": true}
# leggi il file come edge-list: ignora righe che iniziano con '#' e usa whitespace come separatore

cit_hepth = pd.read_csv(
    CITATIONS_DIRECTED_GRAPH, comment="#", sep="\\s+", header=None, engine="python"
)

# Prendiamo le prime due colonne come source/target
citations = cit_heptG.iloc[:, :2].copy()
citations.columns = ["source", "target"]
citations["source"] = pd.to_numeric(citations["source"])
citations["target"] = pd.to_numeric(citations["target"])

del cit_hepth  # non ci serve più

citations_uni = citations.copy()
citations_country = citations.copy()


def safe_get_name(x):
    v = domain_mapping.get(x)
    if isinstance(v, dict):
        return v.get("name")
    return None


def safe_get_country(x):
    v = domain_mapping.get(x)
    if isinstance(v, dict):
        return v.get("country")
    return None


citations_uni["source"] = citations["source"].astype(str).map(safe_get_name)
citations_uni["target"] = citations["target"].astype(str).map(safe_get_name)

citations_country["source"] = citations["source"].astype(str).map(safe_get_country)
citations_country["target"] = citations["target"].astype(str).map(safe_get_country)


# %% jupyter={"source_hidden": true}
citations_uni.dropna().sample(n=3)

# %% jupyter={"source_hidden": true}
citations_country.dropna().sample(n=3)

# %% [markdown]
# ## salvataggio
# %% jupyter={"source_hidden": true}
citations_uni.to_csv(f"{SESSION_PATH}/citations-uni.csv", index=False)
citations_country.to_csv(f"{SESSION_PATH}/citations-country.csv", index=False)

# %% jupyter={"source_hidden": true}
papers.to_csv(f"{SESSION_PATH}/papers.csv", index=False)

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# # EDA

# %% jupyter={"source_hidden": true}
unique = len(
    pd.unique(citations_country[["source", "target"]].dropna().values.ravel("K"))
)
self_loops = len(
    citations_country[
        citations_country["source"] == citations_country["target"]
    ].dropna()
)
edges = len(citations_country.dropna())
print(f"Abbiamo {unique} stati")
print(f"        {edges} archi")
print(f"        {self_loops} self loops")

# %% jupyter={"source_hidden": true}
unique = len(pd.unique(citations_uni[["source", "target"]].dropna().values.ravel("K")))
self_loops = len(
    citations_uni[citations_uni["source"] == citations_uni["target"]].dropna()
)
edges = len(citations_uni.dropna())
print(f"Abbiamo {unique} universita e centri di ricerca")
print(f"        {edges} archi")
print(f"        {self_loops} self loops")

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# # Grafi

# %% [markdown]
# ## Grafi con NaN - no metriche

# %% jupyter={"source_hidden": true}
# per testing e sviluppo delle librerie, rilanciare questo blocco ogni volta che viene
# aggiornata una libreria

# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
graphing = reload(graphing)


# %% [markdown] jp-MarkdownHeadingCollapsed=true
# ### Circular Layout

# %% jupyter={"source_hidden": true}
name = "circular-wpg"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.circular
pos = lay(wpg)
data = graphing.gen_graph_data(wpg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %% [markdown]
# ### ARF Layout

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+

graphing = reload(graphing)
name = "graph-arf-wpg"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.arf
pos = lay(wpg)
data = graphing.gen_graph_data(wpg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %% [markdown]
# ### Kamada Kawai

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+

graphing = reload(graphing)
name = "kamada-wpg"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.kamada
pos = lay(wpg, weight="w")
data = graphing.gen_graph_data(wpg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %% [markdown]
# ### Spring

# %% [markdown]
# #### Base (Auto)

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+

graphing = reload(graphing)
name = "spring-base-wpg"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.spring
pos = lay(wpg, weight="w")
data = graphing.gen_graph_data(wpg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %% [markdown]
# #### Force

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+

graphing = reload(graphing)
name = "spring-force-wpg"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.spring
pos = lay(wpg, weight="w", method="force")
data = graphing.gen_graph_data(wpg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %% [markdown]
# #### Energy

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+

graphing = reload(graphing)
name = "spring-energy-wpg"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.spring
pos = lay(wpg, weight="w", method="energy")
data = graphing.gen_graph_data(wpg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}", show_labels=False)

# %% [markdown]
# Visualizzazione del grafo
# %% [markdown] jp-MarkdownHeadingCollapsed=true
# ## Grafi e metriche con NaN 
# Prima di continuare, bisogna calcolare le metriche

# %% jupyter={"source_hidden": true}
gm = metrics.GraphMetrics(pg, SESSION_PATH)
gm.calc_metrics()

# %% jupyter={"source_hidden": true}
degree_df = pd.DataFrame(gm.degree_cent.items(), columns=['Node', 'DegreeCentrality'])

print(degree_df.sort_values(by='DegreeCentrality', ascending=False).head(11))
print(degree_df.sort_values(by='DegreeCentrality', ascending=True).head(10))

# %% jupyter={"source_hidden": true}
closeness_df = pd.DataFrame(gm.closeness_cent.items(), columns=['Node', 'ClosenessCentrality'])

print(closeness_df.sort_values(by='ClosenessCentrality', ascending=False).head(11))
print(closeness_df.sort_values(by='ClosenessCentrality', ascending=True).head(10))

# %% jupyter={"source_hidden": true}
betweenness_df = pd.DataFrame(gm.betweenness_cent.items(), columns=['Node', 'BetweennessCentrality'])

print(betweenness_df.sort_values(by='BetweennessCentrality', ascending=False).head(11))
print(betweenness_df.sort_values(by='BetweennessCentrality', ascending=True).head(10))

# %% jupyter={"source_hidden": true}
eigenvector_df = pd.DataFrame(gm.eigenvector_cent.items(), columns=['Node', 'EigenvectorCentrality'])

print(eigenvector_df.sort_values(by='EigenvectorCentrality', ascending=False).head(11))
print(eigenvector_df.sort_values(by='EigenvectorCentrality', ascending=True).head(10))

# %% jupyter={"source_hidden": true}
gm = metrics.GraphMetrics(pg, SESSION_PATH)
gm.calc_metrics()

# %% jupyter={"source_hidden": true}
degree_df = pd.DataFrame(gm.degree_cent.items(), columns=['Node', 'DegreeCentrality'])

print(degree_df.sort_values(by='DegreeCentrality', ascending=False).head(11))
print(degree_df.sort_values(by='DegreeCentrality', ascending=True).head(10))

# %% jupyter={"source_hidden": true}
closeness_df = pd.DataFrame(gm.closeness_cent.items(), columns=['Node', 'ClosenessCentrality'])

print(closeness_df.sort_values(by='ClosenessCentrality', ascending=False).head(11))
print(closeness_df.sort_values(by='ClosenessCentrality', ascending=True).head(10))

# %% jupyter={"source_hidden": true}
betweenness_df = pd.DataFrame(gm.betweenness_cent.items(), columns=['Node', 'BetweennessCentrality'])

print(betweenness_df.sort_values(by='BetweennessCentrality', ascending=False).head(11))
print(betweenness_df.sort_values(by='BetweennessCentrality', ascending=True).head(10))

# %% jupyter={"source_hidden": true}
eigenvector_df = pd.DataFrame(gm.eigenvector_cent.items(), columns=['Node', 'EigenvectorCentrality'])

print(eigenvector_df.sort_values(by='EigenvectorCentrality', ascending=False).head(11))
print(eigenvector_df.sort_values(by='EigenvectorCentrality', ascending=True).head(10))

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+
metrics = reload(metrics)
graphing = reload(graphing)

name = "spring-DEGREE"
label = "Degree Centrality"
title = "Spring Layout con Degree Centrality"

pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
lay = graphing.GLAYOUTS.spring 
pos = lay(pg, weight="w", method="energy")

gm = metrics.GraphMetrics(pg, SESSION_PATH)
gm.calc_metrics()
data = graphing.gen_graph_data(pg, pos, gm.degree_cent)
data["node_colors"] = [round(i*100) for i in gm.degree_cent.values()]
graphing.plot_graph(data, label=label, title=title, figsize=graphing.FigSize.XXXL16_9, save_path=f"{SESSION_PATH}/{name}", show_labels=False)

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+
metrics = reload(metrics)
graphing = reload(graphing)

name = "spring-CLOSENESS"
label = "Closeness Centrality"
title = "Spring Layout con Closeness Centrality"

pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
lay = graphing.GLAYOUTS.spring
pos = lay(pg, weight="w", method="energy")

gm = metrics.GraphMetrics(pg, SESSION_PATH)
gm.calc_metrics()
data = graphing.gen_graph_data(pg, pos, gm.closeness_cent)
data["node_colors"] = [round(i*100) for i in gm.closeness_cent.values()]
graphing.plot_graph(data, label=label, title=title,figsize=graphing.FigSize.XXXL16_9, save_path=f"{SESSION_PATH}/{name}", show_labels=False)

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+
metrics = reload(metrics)
graphing = reload(graphing)

name = "spring-BETWEENNESS"
label = "Betweenness Centrality"
title = "Spring Layout con Betweenness Centrality"

pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
lay = graphing.GLAYOUTS.spring
pos = lay(pg, weight="w", method="energy")

gm = metrics.GraphMetrics(pg, SESSION_PATH)
gm.calc_metrics()
data = graphing.gen_graph_data(pg, pos, gm.betweenness_cent)

data["node_colors"] = [round(i*100) for i in gm.betweenness_cent.values()]
graphing.plot_graph(data, label=label, title=title, figsize=graphing.FigSize.XXXL16_9, save_path=f"{SESSION_PATH}/{name}", show_labels=False)

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+
metrics = reload(metrics)
graphing = reload(graphing)

name = "spring-EIGENVECTOR"
label = "Eigenvector Centrality"
title = "Spring Layout con Eigenvector Centrality"


pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
lay = graphing.GLAYOUTS.spring
pos = lay(pg, weight="w", method="energy")

gm = metrics.GraphMetrics(pg, SESSION_PATH)
gm.calc_metrics()
data = graphing.gen_graph_data(pg, pos, gm.eigenvector_cent)

data["node_colors"] = [round(i*100) for i in gm.eigenvector_cent.values()]
graphing.plot_graph(data, label=label, title=title, figsize=graphing.FigSize.XXXL16_9, save_path=f"{SESSION_PATH}/{name}", show_labels=False)

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# ## Grafi e metriche senza NaN 
# Prima di continuare, bisogna calcolare le metriche

# %% jupyter={"source_hidden": true}
G = g.copy()
nan_nodes = []
limit = None
for node in G.nodes():
    if not isinstance(node, str) and matG.isnan(node):
        nan_nodes.append(node)
G.remove_nodes_from(nan_nodes)

if limit:
    sub_nodes = list(G.nodes)[:limit]
    G = G.subgraph(sub_nodes).copy()

M = metrics.GraphMetrics(G, SESSION_PATH)
M.calc_metrics()

# %% jupyter={"source_hidden": true}
metrics = reload(metrics)
graphing = reload(graphing)


name = "spring-DEGREE-no-nan"
label = "Degree Centrality"
title = "Spring Layout con Degree Centrality nnetworkx parallel edges collpase weightnetworkx parallel edges collpase weightN"
pos = graphing.GLAYOUTS.spring(G, k=0.8, iterations=20, method="auto")
# k controls the distance between the nodes and varies between 0 and 1
# iterations is the number of times simulated annealing is run
# default k=0.1 and iterations=50
data = graphing.gen_graph_data(G, pos, M.degree_cent, log_distances=True)
data["node_colors"] = [round(i * 100) for i in M.degree_cent.values()]
graphing.plot_graph(data,
                    label=label,
                    title=title,
                    figsize=graphing.FigSize.XE16_9,
                    save_path=f"{SESSION_PATH}/{name}",
                    show_labels=False
                   )

# %% jupyter={"source_hidden": true}
metrics = reload(metrics)
graphing = reload(graphing)


name = "spring-CLOSENESS-no-nan"
label = "Closeness Centrality"
title = "Spring Layout con Closeness Centrality no NaN"
pos = graphing.GLAYOUTS.spring(G, k=0.8, iterations=20, method="auto")
# k controls the distance between the nodes and varies between 0 and 1
# iterations is the number of times simulated annealing is run
# default k=0.1 and iterations=50
data = graphing.gen_graph_data(G, pos, M.closeness_cent, log_distances=True)
data["node_colors"] = [round(i * 100) for i in M.closeness_cent.values()]
graphing.plot_graph(data,
                    label=label,
                    title=title,
                    figsize=graphing.FigSize.XE16_9,
                    save_path=f"{SESSION_PATH}/{name}",
                    show_labels=False
                   )

# %% jupyter={"source_hidden": true}
metrics = reload(metrics)
graphing = reload(graphing)


name = "spring-BETWEENNESS-no-nan"
label = "Betweenness Centrality"
title = "Spring Layout con Betweenness Centrality no NaN"
pos = graphing.GLAYOUTS.spring(G, k=0.8, iterations=20, method="auto")
# k controls the distance between the nodes and varies between 0 and 1
# iterations is the number of times simulated annealing is run
# default k=0.1 and iterations=50
data = graphing.gen_graph_data(G, pos, M.betweenness_cent, log_distances=True)
data["node_colors"] = [round(i * 100) for i in M.betweenness_cent.values()]
graphing.plot_graph(data,
                    label=label,
                    title=title,
                    figsize=graphing.FigSize.XE16_9,
                    save_path=f"{SESSION_PATH}/{name}",
                    show_labels=False
                   )

# %% jupyter={"source_hidden": true}
metrics = reload(metrics)
graphing = reload(graphing)


name = "spring-EIGENVECTOR-no-nan"
label = "Eigenvector Centrality"
title = "Spring Layout con Eigenvector Centrality no NaN"
pos = graphing.GLAYOUTS.spring(G, k=0.8, iterations=20, method="auto")
# k controls the distance between the nodes and varies between 0 and 1
# iterations is the number of times simulated annealing is run
# default k=0.1 and iterations=50
data = graphing.gen_graph_data(G, pos, M.eigenvector_cent, log_distances=True)
data["node_colors"] = [round(i * 100) for i in M.eigenvector_cent.values()]
graphing.plot_graph(data,
                    label=label,
                    title=title,
                    figsize=graphing.FigSize.XE16_9,
                    save_path=f"{SESSION_PATH}/{name}",
                    show_labels=False
                   )

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# # Metriche
#
# Qua calcoliamo:
# - closeness centrality
# - degree centrality
# - betweenness centrality
# - eigenvector centrality

# %% [markdown]
# ### Definizione funzioni

# %% jupyter={"source_hidden": true}
# per testing e sviluppo delle librerie, rilanciare questo blocco ogni volta che viene
# aggiornata una libreria

# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0


metrics = reload(metrics)

# %% [markdown]
# ### Calcolo Metriche

# %% jupyter={"source_hidden": true}
g = nx.DiGraph()
graphing.add_edges(g, citations_uni)

# %% jupyter={"source_hidden": true}
gm = metrics.GraphMetrics(g, SESSION_PATH)
gm.calc_metrics()

# %% jupyter={"source_hidden": true}
gm.plot_distribution(gm.degree_cent.values(), "Degree Centrality Distribuition", 0.80)

# %% jupyter={"source_hidden": true}
gm.plot_distribution(gm.closeness_cent.values(), "Closeness Centrality Distribuition", 0.80)

# %% jupyter={"source_hidden": true}
gm.plot_distribution(gm.betweenness_cent.values(), "Betweenness Centrality Distribuition", 0.033)

# %% jupyter={"source_hidden": true}
max(gm.betweenness_cent.values())

# %% jupyter={"source_hidden": true}
max(gm.eigenvector_cent.values())

# %% jupyter={"source_hidden": true}
gm.plot_distribution(gm.eigenvector_cent.values(), "Eigenvector Centrality Distribuition", 0.15)

# %% jupyter={"source_hidden": true}
max(gm.indegree.values())

# %% jupyter={"source_hidden": true}
gm.plot_distribution(gm.indegree.values(), "Indegree Distribuition", 0.65)
# %% jupyter={"source_hidden": true}
max(gm.outdegree.values())

# %% jupyter={"source_hidden": true}
gm.plot_distribution(gm.outdegree.values(), "Outdegree Distribuition", 0.85)

# %% jupyter={"source_hidden": true}
max(gm.clustering_coef.values())

# %% jupyter={"source_hidden": true}
gm.plot_distribution(gm.clustering_coef.values(), "Clustering Distribution", 1)

# %% jupyter={"source_hidden": true}
max(gm.pagerank.values())

# %% jupyter={"source_hidden": true}
gm.plot_distribution(gm.pagerank.values(), "Pagerank Distribution", 0.02)

# %% jupyter={"source_hidden": true}
max(gm.k_core.values())

# %% jupyter={"source_hidden": true}
gm.plot_distribution(gm.k_core.values(), "K-Core Distribution", 97)

# %% jupyter={"source_hidden": true}
gm.density

# %% jupyter={"source_hidden": true}
networkx parallel edges collpase weightgm.reciprocity

# %% jupyter={"source_hidden": true}
gm.diameter


# %% [markdown]
# ## Triadi

# %% [markdown]
# il seguente blocco di codice è stato usato per tentare di salvare su file tutte le triadi (nodi ed archi) su file, in quanto la ram non riusciva a tenerle tutte.
# Bene, neanche su file ha senso farlo perchè il totale era arrivato a più di 5GB e stava continuando ad andare. Ho dovuto fermare.

# %% jupyter={"source_hidden": true}
def write_cache(nodes: list, edges: list):
    with open(f"{SESSION_PATH}/triads-nodes.txt", 'a') as f:
        for node_list in nodes:
            f.write(','.join(map(str, node_list)) + '\n')
    with open(f"{SESSION_PATH}/triads-edges.txt", 'a') as f:
        for edge_list in edges:
            f.write(','.join(map(str, edge_list)) + '\n')

tris_nodes = []
tris_edges = []
for i, tri in enumerate(nx.all_triads(g)):
    if i % 5000 == 0 and i > 0:
        write_cache(tris_nodes, tris_edges)
        tris_nodes = []
        tris_edges = []
    tris_nodes.append(list(tri.nodes))
    tris_edges.append(list(tri.edges))

if tris_nodes:
    write_cache(tris_nodes, tris_edges)

# %% jupyter={"source_hidden": true}
# intanto, rimuoviamo il nodo NaN, in questa analisi è fuorviante
G = g.copy()
nan_nodes = []
for node in G.nodes(): 
    if not isinstance(node, str) and matG.isnan(node):
        nan_nodes.append(node)
G.remove_nodes_from(nan_nodes)

# %% jupyter={"source_hidden": true}
print(len(g.nodes) - len(G.nodes)) # nel grafo originale c'è solo un nodo nan
print(len(g.edges) - len(G.edges)) # al quale vi andavano 862 archi (solo?)
# questo tuttavia porta ad un altissimo degree

# %% jupyter={"source_hidden": true}
nx.triadic_census(G)

# %% jupyter={"source_hidden": true}
nx.triadic_census(g)

# %% jupyter={"source_hidden": true}
g.in_edges(nan_nodes[0])

# %% jupyter={"source_hidden": true}
g.out_edges(nan_nodes[0]) 

# %% jupyter={"source_hidden": true}
# test per vedere differenza dello spring con e senza nan
M = metrics.GraphMetrics(G, SESSION_PATH)
M.calc_metrics()

# %% jupyter={"source_hidden": true}
M.plot_distribution(M.degree_cent.values(), "Degree Centrality Distribuition - No NaN", 0.80)

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
metrics = reload(metrics)
graphing = reload(graphing)

name = "spring-DEGREE-no-nan"
label = "Degree Centrality senza NaN"
title = "Spring Layout con Degree Centrality - Grafo senza NaN"

lay = graphing.GLAYOUTS.spring 
pos = lay(G, weight="w", method="energy")
data = graphing.gen_graph_data(G, pos, M.degree_cent)
data["node_colors"] = [round(i*100) for i in M.degree_cent.values()]
graphing.plot_graph(data, label=label, title=title, figsize=graphing.FigSize.XXXL16_9, save_path=f"{SESSION_PATH}/{name}", show_labels=False)

# %% jupyter={"source_hidden": true}
for i, tri in enumerate(nx.all_triads(g))

# %% jupyter={"source_hidden": true}

# %% jupyter={"source_hidden": true}

# %% [markdown]
# ## Clique

# %% [markdown]
# per poter usare enumerate_all_cliques e find_cliques, in networkx, dobbiamo trasformare il grafo da diretto ad indiretto
#
# inoltre ci serve il grafo pesato

# %% jupyter={"source_hidden": true}
graphing = reload(graphing)
H = nx.Graph()
graphing.add_edges_with_weight(H, citations_uni)

# %% jupyter={"source_hidden": true}
G.remove_nodes_from(["other"])

# %% jupyter={"source_hidden": true}
for n in G.nodes:
    G.nodes[n]["weight"] = G.degree(n)

# %% jupyter={"source_hidden": true}
for n in G.nodes:
    G.nodes[n]["weight"] = 1

# %% jupyter={"source_hidden": true}
maximal = 0
allc = 0

# for i in nx.enumerate_all_cliques(H):
#    allc += 1
# TROPPE -> riempe la ram

for i in nx.find_cliques(H):
    maximal += 1
    
maxc, maxn = nx.max_weight_clique(H)


print(f"clique trovate {allc}")
print(f"clique massimali trovate {maximal}")
print(f"clique massima: {maxn} (peso, dove il peso è il degree dei nodi)")
print(f"       numero di nodi nella massimale {len(maxc)}")

# %% [markdown]
# Possiamo già notare che la clique massimale ha un peso totale interessante per essere composta da "soli" 45 nodi. Il sospetto è che nella clique sia presente (ovviamente) il nodo "other".

# %% jupyter={"source_hidden": true}
for i in maxc:
    print(i)

# %% [markdown]
# provando a rimuovere dal grafo il nodo "other" notiamo se ci sono differenze

# %% jupyter={"source_hidden": true}
graphing = reload(graphing)
H = nx.Graph()
graphing.add_edges_with_weight(H, citations_uni, with_nan=False)
for n in G.nodes:
    G.nodes[n]["weight"] = G.degree(n)

# %% jupyter={"source_hidden": true}
maximal = 0
allc = 0



for i in nx.find_cliques(H):
    maximal += 1
    
maxc, maxn = nx.max_weight_clique(H)


print(f"clique trovate {allc}")
print(f"clique massimali trovate {maximal}")
print(f"clique massima: {maxn} (peso, dove il peso è il degree dei nodi)")
print(f"       numero di nodi nella massimale {len(maxc)}")

# %% jupyter={"source_hidden": true}
for i in maxc:
    print(i)

# %% [markdown]
# e pare che cambi solo il punteggio, ma la clique rimane quella.
# Tuttavia il numero di clique massimali ci fa intuire che quello è il minimo numero di clique che possiamo trovare.
# Cercare il massimo, ovviamente, non è pensabile in quanto le risorse computazionali per farlo sono eccessive, ed onestamente inutili (non ci porta informazione).

# %% jupyter={"source_hidden": true}
nx.node_clique_number(H)


# %% jupyter={"source_hidden": true}

# %% [markdown]
# bisogna fare anche K-core

# %% [markdown]
# # Communities

# %% [markdown]
# ATTENZIONE: Grafo H SENZA Nan, Grafo G CON Nan

# %%
def weight_nodes(G):
    for n in G.nodes:
        G.nodes[n]["weight"] = G.degree(n)


# %%
def comm_metrics(S, comm):
    print(f"comunità: {len(comm)}")
    for i, c in enumerate(comm):
        mean_degree = sum([S.nodes()[node]["weight"] for node in c]) / len(c)
        print(f"      community #{i}: {len(c)}")
        print(f"           mean_deg: {round(mean_degree)}")
        print("")
    print("")
    print(f"totale nodi in una comunità {sum([len(c) for c in comm])}")
    print(f"totale nodi nel grafo {S.number_of_nodes()}")


# %%
H = nx.DiGraph()
G = nx.DiGraph()
graphing.add_edges_with_weight(H, citations_uni, with_nan=False) # ci sono nodi che si collegano solo a NaN
# per questo, e per altre ragioni di pulizia del grafo, abbiamo deciso di toglierli
graphing.add_edges_with_weight(G, citations_uni, with_nan=True) # ne teniamo uno di grafo non pulito per fare il confronto
weight_nodes(H)
weight_nodes(G)

# %%
preproc = reload(preproc)
#preproc.node_to_country(H, ror, universities)
preproc.node_to_country_2(H, citations_uni, citations_country)

# %% [markdown]
# Scegliere un algoritmo e poi procedere

# %%
result = nx.community.girvan_newman(H)
communities = next(result)
communities = next(result)
communities = next(result)


# %%
len(communities)

# %%
communities_H = sorted(nx.community.louvain_communities(H), key=len, reverse=True)
communities_G = sorted(nx.community.louvain_communities(G), key=len, reverse=True)

# %%
louvpart_H = sorted(nx.community.louvain_partitions(H), key=len, reverse=True)

# %% [markdown]
# non dimenticare di eseguire anche questo

# %%
graphing.set_node_community(H, communities_H)
graphing.set_edge_community(H)
graphing.set_node_community(G, communities_G)
graphing.set_edge_community(G)

# %%
louvpart_H

# %%
graphing.set_node_community(H, louvpart_H)
graphing.set_edge_community(H)

# %%
print("H - senza NaN".center(50, '-'))
comm_metrics(H, communities_H)
print("G - con NaN".center(50,'-'))
comm_metrics(G, communities_G)

# %%
counting = {}
for i,c in enumerate(communities_H):
    print(f"{i+1}".center(80))
    counting[i] = {}
    for r in c:
        country = H.nodes[r]['country']
        if country not in counting[i]:
            counting[i][country] = {'v': 1}
        else:
            counting[i][country]['v'] += 1
        print(f"{r} - {country}")
    print(counting[i])

# %%
for comm in counting:
    tot = sum(v['v'] for v in counting[comm].values())
    print(tot)
    for v in counting[comm].values():
        v['p'] = 100 * v['v'] / tot
    


# %%
counting

# %%
node_color = [graphing.get_color(H.nodes[v]['community']) for v in H.nodes]
# Set community color for edges between members of the same community (internal) and intra-community edges (external)
external = [(v, w) for v, w in H.edges if H.edges[v, w]['community'] == 0]
internal = [(v, w) for v, w in H.edges if H.edges[v, w]['community'] > 0]
internal_color = ['black' for e in internal]

# %%
sizes = [H.nodes[s]['weight'] + 300 for s in H.nodes]

# %% jupyter={"source_hidden": true}
graphing = reload(graphing)

pos = nx.spring_layout(H, k=0.8, iterations=100)
graphing.plot_community(
    H,
    pos,
    community_colors=node_color,
    external=external,
    internal=internal,
    internal_color=internal_color,
    name="cazzo",
    node_size=sizes,
    figsize=graphing.FigSize.XE16_9
)

# %% jupyter={"source_hidden": true}
graphing = reload(graphing)
graphing.one_by_one_communities(H, communities_H)

# %% jupyter={"source_hidden": true}
graphing = reload(graphing)
graphing.incremental_communities(H, communities_H)

# %% [markdown]
# ## K-core

# %% jupyter={"source_hidden": true}
graphing = reload(graphing)

U = nx.Graph()
graphing.add_edges_with_weight(U, citations_uni)

U.remove_edges_from(nx.selfloop_edges(U))

#for i in range (1,80):
#    print(f"{i} {len(nx.k_core(U, i).nodes)}")

# Create k-core subgraph
k_core = 62
K = nx.k_core(U, k_core)

title = f"Main Core (k = {k_core})"

graphing.plot_k_core_graph(K, title=title, figsize=graphing.FigSize.XE16_9, save_path=f"{SESSION_PATH}/{title}")


# %% jupyter={"source_hidden": true}
graphing = reload(graphing)

U = nx.Graph()
graphing.add_edges_with_weight(U, citations_uni, with_nan=False)

U.remove_edges_from(nx.selfloop_edges(U))

#for i in range (1,80):
#    print(f"{i} {len(nx.k_core(U, i).nodes)}")

# Create k-core subgraph
k_core = 62
K = nx.k_core(U, k_core)

title = f"Main Core (k = {k_core})"

graphing.plot_k_core_graph(K, title=title, figsize=graphing.FigSize.XE16_9, save_path=f"{SESSION_PATH}/{title}")


# %% jupyter={"source_hidden": true}
graphing = reload(graphing)

U = nx.Graph()
graphing.add_edges_with_weight(U, citations_uni, with_nan=False)
weight_nodes(U)
U.remove_edges_from(nx.selfloop_edges(U))


# %% jupyter={"source_hidden": true}
mean_degree = sum(a[1] for a in U.degree)/len(U.degree)

# %% jupyter={"source_hidden": true}
mean_degree = np.median([d for _, d in U.degree])

# %% jupyter={"source_hidden": true}
mean_degree

# %% jupyter={"source_hidden": true}
sorted_nodes = list(sorted(U.degree, key=lambda x: x[1], reverse=True))

# %% jupyter={"source_hidden": true}
error = 50
_err = mean_degree*error/100
mean_upper = mean_degree + _err
mean_lower = mean_degree - _err
print(f"up {mean_upper} - down {mean_lower}")
nodes_outlie_up = [a for a in sorted_nodes if a[1] > mean_upper]
nodes_outlie_down= [a for a in sorted_nodes if a[1] < mean_lower]
nodes_inside = [a for a in sorted_nodes if a[1] < mean_upper and a[1] > mean_lower]
print(f"_")
print(len( nodes_outlie_up))
print(f"|")
print(f"{len(nodes_inside)}")
print(f"|")
print(len( nodes_outlie_down))
print(f"_")

# %% jupyter={"source_hidden": true}
U.remove_nodes_from([a[0] for a in nodes_outlie_up])
U.remove_nodes_from([a[0] for a in nodes_outlie_down])

# %% jupyter={"source_hidden": true}

# %% jupyter={"source_hidden": true}
max_one = sorted_nodes.pop()
U.remove_node(max_one[0])
print(f"{max_one} removed")

# %% jupyter={"source_hidden": true}
#for i in range (1,80):
#    print(f"{i} {len(nx.k_core(U, i).nodes)}")

# Create k-core subgraph
k_core = 90
K = nx.k_core(U, k_core)

title = f"Main Core (k = {k_core})"

graphing.plot_k_core_graph(K, title=title, figsize=graphing.FigSize.XE16_9, save_path=f"{SESSION_PATH}/{title}")


# %% jupyter={"source_hidden": true}
communities_U = sorted(nx.community.louvain_communities(U), key=len, reverse=True)
graphing.set_node_community(U, communities_U)
graphing.set_edge_community(U)

print("U".center(50, '-'))
comm_metrics(U, communities_U)
node_color = [graphing.get_color(U.nodes[v]['community']) for v in U.nodes]
# Set community color for edges between members of the same community (internal) and intra-community edges (external)
external = [(v, w) for v, w in U.edges if U.edges[v, w]['community'] == 0]
internal = [(v, w) for v, w in U.edges if U.edges[v, w]['community'] > 0]
internal_color = ['black' for e in internal]
sizes = [U.nodes[s]['weight'] + 300 for s in U.nodes]

# %% jupyter={"source_hidden": true}
graphing = reload(graphing)

pos = nx.spring_layout(U, k=0.8, iterations=100)
graphing.plot_community(
    U,
    pos,
    community_colors=node_color,
    external=external,
    internal=internal,
    internal_color=internal_color,
    name="cazzo",
    node_size=sizes,
    figsize=graphing.FigSize.XE16_9
)

# %% jupyter={"source_hidden": true}
