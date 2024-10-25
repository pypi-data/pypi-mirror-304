from matplotlib import pyplot as plt
from networkx.classes.digraph import DiGraph
import networkx as nx


def draw_network(the_network: DiGraph, ax: Axis | None = None) -> Axis:
    """Plots the network, bending the double arcs

    :param the_network: network to plot
    :param ax: matplotlib axis object, in case the plot must be included in an existing plot.

    """
    if ax is None:
        fig, ax = plt.subplots()

    nx.draw_networkx_nodes(the_network.nodes, positions, node_color='skyblue')
    return ax
