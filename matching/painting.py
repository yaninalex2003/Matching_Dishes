import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def paint_part_of_graph(dishes, edge_probs, ids = []):
    D1 = nx.Graph()
    ids_draw = ids
    if len(ids_draw) == 0:
        ids_draw = np.random.randint(len(dishes), size = 9)

    draw_dishes = [dishes[i] for i in ids_draw]
    for dish in draw_dishes:
        D1.add_node(dish)
    edge_labels = {}
    for i in ids_draw:
        for j in ids_draw:
            if edge_probs[i][j]:
                D1.add_edge(dishes[i], dishes[j])
                edge_labels[(dishes[i], dishes[j])] = np.around(edge_probs[i][i],3)

    plt.figure(figsize=(6,6))
    pos = nx.circular_layout(D1, scale=0.5)
    nx.draw(D1, pos, with_labels = True, font_size = 10,node_size = 40)
    nx.draw_networkx_edges(D1, pos) 
    nx.draw_networkx_edge_labels(
        D1, pos,
        edge_labels=edge_labels,
        font_color='red',
        verticalalignment  ="bottom"
    )
    plt.show()

def paint_world_cloud(dishes):
    wordcloud = WordCloud(background_color = "white").generate(' '.join(dishes))
    plt.figure(figsize=(8,8))
    plt.axis('off')
    plt.imshow(wordcloud)   
    plt.show()