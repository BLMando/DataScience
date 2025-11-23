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
#     display_name: Python (data env)
#     language: python
#     name: data
# ---

# %% [markdown]
# # Analisi della social network tra istituti di ricerca e università.
# L'obiettivo di questa analisi è quella di individuare se, all'interno della comunità scientifica, esistano
# dei gruppi naturali (comunità) tra i diversi istituti di ricerca nel campo della Energia.
# %%
# Importiamo tutte le dipendenze

from importlib import reload
from datetime import datetime
from pathlib import Path
from tqdm.notebook import tqdm
import utils.graphing as graphing
import utils.metrics as metrics
import networkx as nx
import os
import pandas as pd
import utils.preproc as preproc
import warnings


CITATIONS_DIRECTED_GRAPH = "./data/cit-HepTh.txt"
CITATIONS_ABSTRACTS_DIR = "./data/cit-HepTh-abstracts"

ROR_DATA = "./data/ror-data.csv"
UNIVERSITIES_DATA = "./data/all_universities.csv"

warnings.filterwarnings("ignore")

# %% [markdown]
# Questa linea genera la session_id. Se la sovrascrivi si intende che hai fatto cambiamenti al dataset
# perciò il resto del codice non farà più affidamento alla sessione precedente e quindi alcuni file
# vanno rigenerati
#
# Se invece vuoi usare una session precedente, usa il blocco sotto e definisci manualmente il numero di sessione
#
# %% jupyter={"source_hidden": false}
s = datetime.now().strftime("%y%m%d%H%M")
session_id = f"{s}"  # NUOVA SESSIONE
SESSION_PATH = f"data/sessions/{session_id}"
os.makedirs(SESSION_PATH, exist_ok=True)

# %% jupyter={"source_hidden": false}
session_id = "2511212247"  # RICARICA UNA SESSIONE
SESSION_PATH = f"data/sessions/{session_id}"

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# # Preprocessamento
# eseguiamo le operazioni preliminari di caricamento dei dati
#
# citations contiene il grafo diretto con colonne target e source
# %% jupyter={"source_hidden": false}
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

# %% [markdown]
# Mapping dei paper alle rispettive università
# %%
ror = pd.read_csv(ROR_DATA)
ror["clean_url"] = (
    ror["links"].str.replace(r"^https?://", "", regex=True).str.split("/").str[0]
)
ror["tld2"] = ror["clean_url"].str.extract(r"([a-zA-Z0-9-]+\.[a-zA-Z0-9-]+)$")

universities = pd.read_csv(UNIVERSITIES_DATA)

domain_mapping = {
    str(row.id): preproc.extract_domain(row.email, ror, universities)
    for row in tqdm(papers.itertuples())
}

# %%
# leggi il file come edge-list: ignora righe che iniziano con '#' e usa whitespace come separatore

cit_hepth = pd.read_csv(
    CITATIONS_DIRECTED_GRAPH, comment="#", sep="\\s+", header=None, engine="python"
)

# Prendiamo le prime due colonne come source/target
citations = cit_hepth.iloc[:, :2].copy()
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


# %%
citations_uni.dropna().sample(n=3)

# %%
citations_country.dropna().sample(n=3)

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# # SALVATAGGIO o CARICAMENTO
# %% [markdown]
# ## salvataggio
# %%
citations_uni.to_csv(f"{SESSION_PATH}/citations-uni.csv", index=False)
citations_country.to_csv(f"{SESSION_PATH}/citations-country.csv", index=False)

# %%
papers.to_csv(f"{SESSION_PATH}/papers.csv", index=False)

# %% [markdown]
# ## caricamento
# %%
citations_uni = pd.read_csv(f"{SESSION_PATH}/citations-uni.csv")
citations_country = pd.read_csv(f"{SESSION_PATH}/citations-country.csv")
# %%
papers = pd.read_csv(f"{SESSION_PATH}/papers.csv")

# %% [markdown]
# # Grafi

# %%
# per testing e sviluppo delle librerie, rilanciare questo blocco ogni volta che viene
# aggiornata una libreria

# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0


graphing = reload(graphing)


# %% [markdown]
# ## Circular Layout

# %%
name = "circular-wpg"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.circular
pos = lay(wpg)
data = graphing.gen_graph_data(wpg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %% [markdown]
# ## ARF Layout

# %%
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

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+

graphing = reload(graphing)
name = "graph-bfs"

pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.bipartite
pos = lay(pg)
data = graphing.gen_default(pg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+

graphing = reload(graphing)
name = "graph-bfs"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.bfs
pos = lay(pg)
data = graphing.gen_default(pg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %%
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

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+

graphing = reload(graphing)
name = "planar"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.planar
pos = lay(pg)
data = graphing.gen_default(pg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %%
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

# %%
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

# %%
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

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+

graphing = reload(graphing)
name = "spiral"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.spiral
pos = lay(pg, resolution=1)
data = graphing.gen_graph_data(pg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %% jupyter={"source_hidden": true}
# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0
from importlib import reload  # Python 3.4+

graphing = reload(graphing)
name = "spiral-equidistant"
pg = nx.DiGraph()
graphing.add_edges(pg, citations_uni)
wpg = graphing.edge_collapse(pg, nx.DiGraph)
lay = graphing.GLAYOUTS.spiral
pos = lay(pg, resolution=1, equidistant=True)
data = graphing.gen_graph_data(pg, pos)
graphing.plot_graph(data, save_path=f"{SESSION_PATH}/{name}")

# %% [markdown]
# Visualizzazione del grafo
# %%
unique = len(pd.unique(citations_uni[["source", "target"]].dropna().values.ravel("K")))
self_loops = len(
    citations_uni[citations_uni["source"] == citations_uni["target"]].dropna()
)
edges = len(citations_uni.dropna())
print(f"Abbiamo {unique} universita e centri di ricerca")
print(f"        {edges} archi")
print(f"        {self_loops} self loops")

# %%
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

# %% [markdown]
# # GRAFI CON METRICHE
# Prima di continuare, bisogna calcolare le metriche

# %%
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
data = graphing.gen_graph_data(pg, pos, gm.degree_cent)
gm = metrics.GraphMetrics(pg, SESSION_PATH)
gm.calc_metrics()
data["node_colors"] = [round(i*100) for i in gm.degree_cent.values()]
graphing.plot_graph(data, label=label, title=title, save_path=f"{SESSION_PATH}/{name}", show_labels=False)

# %%
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
data = graphing.gen_graph_data(pg, pos)
gm = metrics.GraphMetrics(pg, SESSION_PATH)
gm.calc_metrics()
data["node_colors"] = [round(i*100) for i in gm.closeness_cent.values()]
graphing.plot_graph(data, label=label, title=title, save_path=f"{SESSION_PATH}/{name}", show_labels=False)

# %%
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

# %%
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

# %%

# %% [markdown]
# # Metriche
#
# Qua calcoliamo:
# - closeness centrality
# - degree centrality
# - betweenness centrality
# - eigenvector centrality

# %% [markdown]
# ### Definizione funzioni

# %%
# per testing e sviluppo delle librerie, rilanciare questo blocco ogni volta che viene
# aggiornata una libreria

# Source - https://stackoverflow.com/a/437591
# Posted by cdleary, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-21, License - CC BY-SA 4.0


metrics = reload(metrics)

# %% [markdown]
# ### Calcolo Metriche

# %%
g = nx.DiGraph()
graphing.add_edges(g, citations_uni)

gm = metrics.GraphMetrics(g, SESSION_PATH)
gm.calc_metrics()

# %% jupyter={"outputs_hidden": true}
gm.plot_distribution(gm.degree_cent.values(), "Degree Centrality Distribuition", 0.80)

# %% jupyter={"outputs_hidden": true}
gm.plot_distribution( gm.closeness_cent.values(), "Closeness Centrality Distribuition", 0.80)

# %% jupyter={"outputs_hidden": true}
gm.plot_distribution( gm.betweenness_cent.values(), "Betweenness Centrality Distribuition", 0.033)

# %%
max(gm.betweenness_cent.values())

# %%
max(gm.eigenvector_cent.values())

# %% jupyter={"outputs_hidden": true}
gm.plot_distribution( gm.eigenvector_cent.values(), "Eigenvector Centrality Distribuition", 0.15)

# %%
max(gm.indegree.values())

# %% jupyter={"outputs_hidden": true}
gm.plot_distribution(gm.indegree.values(), "Indegree Distribuition", 0.65)
# %%
max(gm.outdegree.values())

# %% jupyter={"outputs_hidden": true}
gm.plot_distribution(gm.outdegree.values(), "Outdegree Distribuition", 0.85)

# %%
max(gm.clustering_coef.values())

# %% jupyter={"outputs_hidden": true}
gm.plot_distribution(gm.clustering_coef.values(), "Clustering Distribution", 1)

# %%
max(gm.pagerank.values())

# %% jupyter={"outputs_hidden": true}
gm.plot_distribution(gm.pagerank.values(), "Pagerank Distribution", 0.02)

# %%
max(gm.k_core.values())

# %% jupyter={"outputs_hidden": true}
gm.plot_distribution(gm.k_core.values(), "K-Core Distribution", 97)

# %%
gm.density

# %%
gm.reciprocity

# %%
gm.diameter

# %% [markdown]
# ## Triadi

# %%
nx.triadic_census(g)

# %%
nx.triads_by_type(g)

# %%
