import json
import geopandas as gpd
import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx
from networkx.readwrite import json_graph


def read_file(path):
    data = gpd.read_file(path)
    return data


def add_one_poly(index, poly, edges):
    vtx = list(poly.exterior.coords)
    vtx.append(vtx[0])
    for i in range(len(vtx) - 1):
        edges[index].add(vtx[i])


def draw_graph(center, fig_path, rate_type):
    plt.clf()
    centroid, geometry, node_idx = center['centroid'], center['geometry'], [index for index, _ in center.iterrows()]
    rate = center[rate_type]
    edges = defaultdict(set)

    # the edges for each district
    # actually are the vertices of each area polygon
    # using edges to determine adjacency has problem so use vertices instead
    for i in node_idx:
        multi_or_single = geometry[i]
        try:
            add_one_poly(i, multi_or_single, edges)
        except AttributeError:
            for single in multi_or_single.geoms:
                add_one_poly(i, single, edges)

    G = nx.Graph()

    # each district as a node
    for index, row in center.iterrows():
        G.add_node(index, pos=(row['centroid'].x, row['centroid'].y), rate=row[rate_type])
    # the position of each node
    pos = nx.get_node_attributes(G, 'pos')

    # edges for the graph
    for i in range(len(node_idx)):
        for j in range(i + 1, len(node_idx), 1):
            node_i = node_idx[i]
            node_j = node_idx[j]
            connect = False
            # check if two regions have the same vertex
            for edge_i in edges[node_i]:
                if edge_i in edges[node_j]:
                    connect = True
                    break
            if connect:
                G.add_edge(node_i, node_j)

    options = {
        "font_size": 36,
        "node_size": 150,
        "edge_color": "#a9dfda",
        "node_color": "#2eae8f",
        "linewidths": 1,
        "width": 2,
    }
    nx.draw(G, pos, **options)

    labels = dict(zip(node_idx, rate))
    nx.draw_networkx_labels(G, pos, labels, font_size=4, font_color="whitesmoke")
    plt.savefig(fig_path, dpi=600)
    return G


def draw_map(center, fig_path, rate_type):
    plt.clf()
    center.plot(
        column='ACNUMBER', cmap='Blues',
        linewidth=0.2, edgecolor='0.5')
    for index, row in center.iterrows():
        xy = row['centroid'].coords[:]
        plt.annotate(
            row[rate_type], xy=xy[0],
            ha='center', va='center',
            size=3)
    plt.savefig(fig_path, dpi=600)


if __name__ == "__main__":
    path_to_center = 'data/halifax_center/halifax_center.shp'
    center = read_file(path_to_center)
    # change crs to calculate centroid for each district
    center_proj = center.to_crs('epsg:4087')
    center_proj['centroid'] = center_proj['geometry'].centroid.to_crs('EPSG:4326')
    center = center_proj.to_crs('EPSG:4326')
    # draw the graph based on month rate
    G_month = draw_graph(center, "image/graph_month.png", 'MRATE')
    draw_map(center, "image/map_month.png", 'MRATE')   # map corresponding to the graph
    Gm_json = json_graph.node_link_data(G_month)
    with open('data/graph_month.json', 'w') as f:
        json.dump(Gm_json, f)
    # draw the graph based on month rate
    G_day = draw_graph(center, "image/graph_day.png", 'DRATE')
    draw_map(center, "image/map_day.png", 'DRATE') # map corresponding to the graph
    Gd_json = json_graph.node_link_data(G_day)
    with open('data/graph_day.json', 'w') as f:
        json.dump(Gd_json, f)
