import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np
import textwrap
from typing import Dict, Mapping, Hashable


class GraphMetrics:
    degree_cent: Dict[Hashable, float]
    closeness_cent: Dict[Hashable, float]
    betweenness_cent: Dict[Hashable, float]
    eigenvector_cent: Dict[Hashable, float]
    indegree: Dict[Hashable, float]
    outdegree: Dict[Hashable, float]
    pagerank: Dict[Hashable, float]
    k_core: Dict[Hashable, int]
    clustering_coef: float | int | Dict[Hashable, float]
    density: float
    diameter: int | None
    path_length: Mapping[Hashable, Dict[Hashable, int]]
    modularity: np.ndarray | None
    reciprocity: float | dict[Hashable, float | None]
    SESSION_PATH: str
    _G: nx.Graph

    def __init__(self, G, SESSION_PATH) -> None:
        self._G = G
        self.SESSION_PATH = SESSION_PATH

    def calc_metrics(self) -> None:
        self.degree_cent = nx.degree_centrality(self._G)
        self.closeness_cent = nx.closeness_centrality(self._G)
        self.betweenness_cent = nx.betweenness_centrality(self._G)
        self.eigenvector_cent = nx.eigenvector_centrality(self._G)
        self.indegree = nx.in_degree_centrality(self._G)
        self.outdegree = nx.out_degree_centrality(self._G)
        self.pagerank = nx.pagerank(self._G)

        H = self._G.copy()
        H.remove_edges_from(nx.selfloop_edges(H))
        self.k_core = nx.core_number(H)

        self.clustering_coef = nx.clustering(self._G)
        self.density = nx.density(self._G)

        if isinstance(self._G, nx.DiGraph):
            if nx.is_strongly_connected(self._G):
                self.diameter = nx.diameter(self._G)
            else:
                self.diameter = None

        self.path_length = dict(nx.all_pairs_shortest_path_length(self._G))

        if not isinstance(self._G, nx.DiGraph):
            self.modularity = nx.modularity_matrix(self._G)
        else:
            self.modularity = None
        self.reciprocity = nx.reciprocity(self._G)

    def plot_distribution(self, values, title, scale=0.5, path=None):
        if not path:
            path = self.SESSION_PATH

        fig, ax = plt.subplots(figsize=(15, 5))

        values = sorted(values)
        n = len(values)
        bin_width = 3.5 * np.std(values) / (n ** (1 / 3))
        numero_bin = int((max(values) - min(values)) / bin_width) * 3

        sns.histplot(values, kde=True, bins=numero_bin, ax=ax)
        # plt.xticks(rotation=80, fontsize=8, ax=ax)
        ax.set_ylabel("Numero Università", fontsize=11)
        # ax.xlabel("Centralità", fontsize=11)

        ax.axvline(x=np.mean(values), color="red", ls="--", lw=2, label="Media")  # pyright: ignore[reportArgumentType]
        ax.set_title(title, fontsize=12)
        ax.legend(loc="upper right")  # bbox_to_anchor=(1.0, 1),

        # if opzione != "clustering":
        #     ax.set_xlim(0, 80)
        # else:
        ax.set_xlim(0, scale)

        plt.savefig(path + "/" + title + ".png", format="png", bbox_inches="tight")
        plt.show()






    # ----------------- print report

    def _print_title(self, title: str):
        print(f"{title.center(80, '-')}")

    def _print_content(self, content: str, sub_level=1) -> None:
        _base_level = max([sub_level, 1]) * 10
        lines = textwrap.wrap(content, 50, break_long_words=False)
        for line in lines:
            print(f"{line.ljust(_base_level)}")

    def _print_paragraph(self, title, content):
        self._print_title(title)
        print("")
        self._print_content(content)
        print("")

    def _sort_metric(self, metric):
        sort = sorted(metric.items(), key=lambda x: x[1], reverse=True)
        if not sort[0][0]:
            sort.pop(0)
        top = []
        last = []
        top.append(sort[0][1])
        top.append(sort[1][1])
        top.append(sort[2][1])
        last.append(sort[-1][1])
        last.append(sort[-2][1])
        last.append(sort[-3][1])

        return (top, last)

    def _print_metric(self, metric):
        top, last = self._sort_metric(metric)
        content = f"Top 3: {top}\nLeast 3: {last}\n"

        try:
            mean = np.mean(list(metric.values())) # # pyright: ignore[reportAttributeAccessIssue]
            content += f"Mean: {mean}"
        except Exception:
            pass

        self._print_paragraph("DEGREE CENTRALITY", content)


    def report(self):
        # degree centrality
        self._print_metric(self.degree_cent)
        self._print_metric(self.closeness_cent)
        self._print_metric(self.betweenness_cent)
        self._print_metric(self.eigenvector_cent)
        self._print_metric(self.indegree)
        self._print_metric(self.outdegree)
        self._print_metric(self.pagerank)
        self._print_metric(self.k_core)

        # clustering coefficient
        cc2 = self.clustering_coef
        self._print_paragraph(
            "CLUSTERING COEFFICIENT",
            f"value: {cc2}",
        )

        # density
        self._print_paragraph("GRAPH DENSITY", f"Density: {self.density}")

        # diameter
        self._print_paragraph("DIAMETER", f"Diameter: {self.diameter}")

        # reciprocity
        self._print_paragraph("RECIPROCITY", f"Reciprocity: {self.reciprocity}")
