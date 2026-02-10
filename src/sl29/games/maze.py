"""Module providing the Maze class"""
import plotly.graph_objects as go
import networkx as nx
import random

class Maze:
    """Class representing a maze"""

    def __init__(self, width, length, height=1, density = 0):
        """Initialize the maze with a 2D list of characters"""
        self.width = width
        self.length = length
        self.height = height
        self.density = density
        # 1. Create a 3D grid graph where each node has edges to its adjacent nodes (up, down, left, right, and optionally up/down in 3D)
        self.graph = nx.grid_graph(dim=[width, length, height])

        # 2. Assign a Cell object to each node in the graph
        for node in self.graph.nodes():
            x, y, z = node # the id of the node is a tuple (x,y,z)
            self.graph.nodes[node]['data'] = Cell(node)

        # 3. Remove all edges to start with a maze full of walls
        self.graph.remove_edges_from(list(self.graph.edges()))

        self.create_maze()

    def create_maze(self):
        def _recur_maze(graph,long,lar,haut,density = 0.0):
            if long == 1 and lar == 1 and haut == 1:
                return graph
            else:
                nodes = graph.nodes
                nodes_list = sorted([node for node in nodes])
                min_z,min_y,min_x = nodes_list[0]
                if long >= lar and long >= haut:
                    # Division
                    nodes_a = [node for node in nodes if node[2] < (min_x + (long // 2))]
                    nodes_b = [node for node in nodes if node[2] >= (min_x + (long // 2))]
                    # Sous graphes
                    graph1 = graph.subgraph(nodes_a).copy()
                    graph2 = graph.subgraph(nodes_b).copy()
                    # Appels récursifs
                    graph1 = _recur_maze(graph1,(long//2),lar,haut,density)
                    graph2 = _recur_maze(graph2,((long//2)+long%2),lar,haut,density)
                    # Fusion
                    fused_graph = nx.compose(graph1, graph2)
                    # Calcul du nombre de portes
                    nb_portes = round(lar * haut * density)
                    if nb_portes == 0: nb_portes = 1
                    for _ in range(nb_portes):
                        # Randomization de la porte
                        y_plus = random.randint(0,lar-1)
                        z_plus = random.randint(0,haut-1)
                        # Ajout du passage
                        fused_graph.add_edge((min_z + z_plus,min_y + y_plus,min_x + (long//2)-1),(min_z + z_plus,min_y + y_plus,min_x + (long//2)))
                    return fused_graph
                if lar >= long and lar >= haut:
                    # Division
                    nodes_a = [node for node in nodes if node[1] < (min_y + (lar // 2))]
                    nodes_b = [node for node in nodes if node[1] >= (min_y + (lar // 2))]
                    # Sous graphes
                    graph1 = graph.subgraph(nodes_a).copy()
                    graph2 = graph.subgraph(nodes_b).copy()
                    # Appels récursifs
                    graph1 = _recur_maze(graph1,long,(lar//2),haut,density)
                    graph2 = _recur_maze(graph2,long,((lar//2)+lar%2),haut,density)
                    # Fusion et ajout du passage
                    fused_graph = nx.compose(graph1, graph2)
                    # Calcul du nombre de portes
                    nb_portes = round(long * haut * density)
                    if nb_portes == 0: nb_portes = 1
                    for _ in range(nb_portes):
                        # Randomization de la porte
                        x_plus = random.randint(0,long-1)
                        z_plus = random.randint(0,haut-1)
                        # Ajout du passage
                        fused_graph.add_edge((min_z + z_plus,min_y + (lar//2)-1,min_x + x_plus),(min_z + z_plus,min_y + (lar//2),min_x + x_plus))
                    return fused_graph
                else:
                    return graph
        
        self.graph = _recur_maze(self.graph,self.width,self.length,self.height,self.density)

class Cell:
    """Class representing a cell in the maze"""

    def __init__(self, coords):
        """Initialize the cell with its coordinates"""
        self.coords = coords #(x,y,z)


def plot_interactive_3d(maze):
    edge_x, edge_y, edge_z = [], [], []
    
    for edge in maze.graph.edges():
        edge_x.extend([edge[0][0], edge[1][0], None])
        edge_y.extend([edge[0][1], edge[1][1], None])
        edge_z.extend([edge[0][2], edge[1][2], None])

    fig = go.Figure(data=[go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='black', width=4)
    )])
    fig.show()

if __name__ == '__main__':
    maze = Maze(20,20,density=0.2)
    plot_interactive_3d(maze)