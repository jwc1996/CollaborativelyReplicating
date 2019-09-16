from __future__ import division

__author__ = 'leaf'

import networkx as nx
import matplotlib.pyplot as plt
import random
from time import time

start = time()
print("Start: " + str(start))

number_node = 5000

G = nx.generators.directed.random_k_out_graph(number_node, 4, 1)
pos = nx.layout.spring_layout(G)

node_sizes = [3 + 10 * i for i in range(len(G))]
M = G.number_of_edges()
edge_colors = range(2, M + 2)
edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')
edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->',
                               arrowsize=10, edge_color=edge_colors,
                               edge_cmap=plt.cm.Blues, width=2)
# set alpha value for each edge
# for i in range(M):
#    edges[i].set_alpha(edge_alphas[i])

ax = plt.gca()
ax.set_axis_off()

# plt.show()
plt.savefig('./generated_image.png')

stop = time()
print("Stop: " + str(stop))
print(str(stop - start) + "seconds")

# print(list(G.nodes))
# print(list(G.edges()))
# print(list(G.edges(0 ))[0][1])

actual_degrees = [d for v, d in G.degree()]

print(actual_degrees)

# select source node
times = 200
path_len = 10000

with open('path_%d.csv' % number_node, 'w') as f:
    for i in range(times):
        stop = time()
        print(i, str(stop - start) + "seconds")

        path = []
        source_index = random.randint(0, number_node - 1)
        path.append(source_index)
        count = 1
        while count < path_len:
            temp_choice = list(G.edges(source_index))
            # print(temp_choice)
            temp_index = list(set([x for (s, x) in temp_choice]))
            # print(temp_index)

            len_temp_index = len(temp_index)

            source_index = temp_index[random.randint(0, len_temp_index - 1)]

            path.append(source_index)

            # print("Hello",source_index)
            count = count + 1

        # print("path", path)
        f.write(','.join(str(e) for e in path))
        f.write('\n')
