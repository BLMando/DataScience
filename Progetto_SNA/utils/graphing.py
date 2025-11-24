from enum import Enum
from dataclasses import dataclass
import pandas as pd
import traceback
from networkx.algorithms import boundary
from numpy import log, nan
from typing import Callable, Iterable
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib import colormaps
from enum import Enum


def _to_inch(n, dpi=300) -> float:
    return round(n / dpi, 1)


def PixToInch(width, height, dpi):
    return (_to_inch(width, dpi), _to_inch(height, dpi))


class FigSize(Enum):
    _dpi = 300
    DPI = _dpi
    AUTO = None
    XXS1_1 = PixToInch(500, 500, _dpi)
    XS1_1 = PixToInch(1000, 1000, _dpi)
    S1_1 = PixToInch(1500, 1500, _dpi)
    M1_1 = PixToInch(2000, 2000, _dpi)
    L1_1 = PixToInch(2500, 2500, _dpi)
    XL1_1 = PixToInch(3000, 3000, _dpi)
    XXL1_1 = PixToInch(5000, 5000, _dpi)
    XXXL1_1 = PixToInch(10000, 10000, _dpi)
    ENORMOUS1_1 = PixToInch(15000, 15000, _dpi)
    XE1_1 = PixToInch(50000, 50000, _dpi)

    XXS16_9 = PixToInch(500, 281, _dpi)
    XS16_9 = PixToInch(1000, 562, _dpi)
    S16_9 = PixToInch(1500, 844, _dpi)
    M16_9 = PixToInch(2000, 1125, _dpi)
    L16_9 = PixToInch(2500, 1406, _dpi)
    XL16_9 = PixToInch(3000, 1688, _dpi)
    XXL16_9 = PixToInch(3500, 1969, _dpi)
    XXXL16_9 = PixToInch(4000, 2250, _dpi)
    ENORMOUS16_9 = PixToInch(5000, 2812, _dpi)
    XE16_9 = PixToInch(10000, 5625, _dpi)

    XXS4_3 = PixToInch(500, 375, _dpi)
    XS4_3 = PixToInch(1000, 750, _dpi)
    S4_3 = PixToInch(1500, 1125, _dpi)
    M4_3 = PixToInch(2000, 1500, _dpi)
    L4_3 = PixToInch(2500, 1875, _dpi)
    XL4_3 = PixToInch(3000, 2250, _dpi)
    XXL4_3 = PixToInch(3500, 2625, _dpi)
    XXXL4_3 = PixToInch(4000, 3000, _dpi)
    ENORMOUS4_3 = PixToInch(5000, 3750, _dpi)
    XE4_3 = PixToInch(10000, 7500, _dpi)


class GLAYOUTS(Enum):
    arf: Callable = nx.arf_layout
    bipartite: Callable = nx.bipartite_layout
    # bfs: Callable = nx.bfs_layout
    circular: Callable = nx.circular_layout
    # forceatlas2: Callable = nx.forceatlas2_layout
    kamada: Callable = nx.kamada_kawai_layout
    planar: Callable = nx.planar_layout
    random: Callable = nx.random_layout
    rescale: Callable = nx.rescale_layout
    rescale_dict: Callable = nx.rescale_layout_dict
    shell: Callable = nx.shell_layout
    spring: Callable = nx.spring_layout
    spectral: Callable = nx.spectral_layout
    spiral: Callable = nx.spiral_layout
    multipartite: Callable = nx.multipartite_layout


class CMAP(str, Enum):
    VIRIDIS = "viridis"
    PLASMA = "plasma"
    INFERNO = "inferno"
    MAGMA = "magma"
    CIVIDIS = "cividis"
    COOLWARM = "coolwarm"
    JET = "jet"
    GREENS = "Greens"
    BLUES = "Blues"


def clamp(value, min_value, max_value):
    return max(min(int(value), max_value), min_value)


def gen_graph_data(G, pos, metric, log_distances=False):
    if not pos:
        pos = GLAYOUTS.kamada(G)
    if not metric:
        metric = dict(G.degree())

    # Apply logarithmic transformation to distances if requested
    if log_distances:
        center = np.array([0, 0])
        pos_transformed = {}
        for node, coord in pos.items():
            coord_array = np.array(coord)
            distance = np.linalg.norm(coord_array - center)
            if distance > 0:
                direction = (coord_array - center) / distance
                log_distance = np.log1p(distance)
                pos_transformed[node] = tuple(center + direction * log_distance)
            else:
                pos_transformed[node] = coord
        pos = pos_transformed

    node_sizes = []
    data_alpha = []
    node_colors = []
    min_metric = min(metric.values())
    max_metric = max(metric.values())

    non = G.number_of_nodes()

    def _era_facile(num, max_num):
        return 100 * num / max_num * (30 + non / 10)

    for n in G.nodes():
        node_sizes.append(max(_era_facile(metric[n], max_metric), 30 + non / 10))
        data_alpha.append(1)
        node_colors.append(metric[n])

    return {
        "G": G,
        "pos": pos,
        "degrees": metric,
        "metric": metric,
        "node_sizes": node_sizes,
        "node_colors": node_colors,
        "alpha": data_alpha,
        "cmap": CMAP.COOLWARM,
    }


def block(func):
    return func()


def plot_graph(
    data,
    figsize=FigSize.AUTO,
    dpi=FigSize.DPI.value,
    save_path=None,
    show_labels=False,
    title="Graph",
    label="Label",
    opts={},
):
    try:
        n = data["G"].number_of_nodes()
        if figsize == FigSize.AUTO:
            avg = sum(data["node_sizes"]) / n
            density = n / avg
            print(f"{density}")

            # this function is defined here becouse python has no proper lambda function support (no multiline)
            def _size(nodes):
                match nodes:
                    case v if v < 0.5:
                        return FigSize.M16_9
                    case v if v < 0.6:
                        return FigSize.L16_9
                    case v if v < 0.7:
                        return FigSize.XL16_9
                    case v if v < 0.8:
                        return FigSize.XXL16_9
                    case v if v < 1:
                        return FigSize.XXXL16_9
                    case _:
                        return FigSize.XE16_9

            figsize = _size(density)

        print(figsize)
        edge_colors = range(2, n + 2)
        plt.figure(figsize=figsize.value, dpi=dpi)

        nodes = nx.draw_networkx_nodes(
            data["G"],
            data["pos"],
            node_size=data["node_sizes"],
            node_color=data["node_colors"],
            cmap=data["cmap"],
            alpha=1,
            linewidths=1,
            edgecolors="black",
        )

        nx.draw_networkx_edges(
            data["G"],
            data["pos"],
            arrowsize=5,
            edge_color="gray",
            alpha=0.5,
            width=0.15,
        )

        if show_labels:
            nx.draw_networkx_labels(
                data["G"], data["pos"], font_size=7, font_color="black"
            )

        cbar = plt.colorbar(nodes)
        cbar.set_label(f"{label}")

        # all_values = data["metric"].values
        #
        # step = 0.1
        # steps = 5
        #
        # boundaries = [a * step for a in range(0, round(steps) + 1)]
        #
        # cmap = plt.cm.inferno
        # norm = BoundaryNorm(boundaries, cmap.N)
        #
        # img = plt.imshow([[0, 1], [2, 3]], cmap=cmap, norm=norm)
        #
        # cbar = plt.colorbar(img)
        # cbar.boundaries = boundaries

        if title:
            plt.title(title)

        plt.axis("off")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=dpi, bbox_inches="tight")

        plt.show()
    except Exception:
        print(traceback.format_exc())


def add_edges(G: nx.Graph, df):
    # for _, row in df.dropna().iterrows():
    #     G.add_edge(row["source"], row["target"])
    G.add_edges_from(list(df.itertuples(index=False)))


def add_edges_with_weight(G: nx.Graph, df):
    for src, dst in df.itertuples(index=False):
        if pd.isna(src):
            src = "other"
        if pd.isna(dst):
            dst = "other"

        if G.has_edge(src, dst):
            G[src][dst]["weight"] += 1
        else:
            G.add_edge(src, dst, weight=1)


def edge_collapse(G: nx.MultiGraph, type: Callable = nx.MultiDiGraph):
    H = type()
    for u, v in G.edges():
        if H.has_edge(u, v):
            H[u][v]["w"] += 1
        else:
            H.add_edge(u, v, w=1)
    return H
