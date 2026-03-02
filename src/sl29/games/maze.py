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
        def _recur_maze(graph,tuple_tailles,density = 0.0):
            def _sous_recur(graph,tuple_coor:tuple[tuple[int]],nb,density = 0.0):
                nodes = graph.nodes
                # Division
                nodes_a = [node for node in nodes if node[nb] < (tuple_coor[nb][0] + (tuple_coor[nb][1] // 2))]
                nodes_b = [node for node in nodes if node[nb] >= (tuple_coor[nb][0] + (tuple_coor[nb][1] // 2))]
                # Sous graphes
                graph1 = graph.subgraph(nodes_a).copy()
                graph2 = graph.subgraph(nodes_b).copy()
                # Appels récursifs
                tuple_taille_1 = tuple([tuple_coor[i][1] if i != nb else tuple_coor[i][1]//2 for i in range(len(tuple_coor))])
                tuple_taille_2 = tuple([tuple_coor[i][1] if i != nb else tuple_coor[i][1]//2 + tuple_coor[i][1]%2 for i in range(len(tuple_coor))])
                graph1 = _recur_maze(graph1,tuple_taille_1,density)
                graph2 = _recur_maze(graph2,tuple_taille_2,density)
                # Fusion et ajout du passage
                fused_graph = nx.compose(graph1, graph2)
                # Calcul du nombre de portes
                nb_portes = round(tuple_coor[(nb+1)%3][1] * tuple_coor[(nb+2)%3][1] * density)
                if nb_portes == 0: nb_portes = 1
                for _ in range(nb_portes):
                    # Randomization de la porte
                    nouv_z,nouv_y,nouv_x = (tuple_coor[i][0] + random.randint(0,tuple_coor[i][1]-1) if i != nb else tuple_coor[i][0] + (tuple_coor[i][1]//2)-1 for i in range(len(tuple_coor)))
                    # Ajout du passage
                    fused_graph.add_edge((nouv_z,nouv_y,nouv_x),(nouv_z,nouv_y+1,nouv_x))
                return fused_graph
            
            if tuple_tailles == (1,1,1):
                return graph
            else:
                haut,lar,long = tuple_tailles
                nodes_list = sorted([node for node in graph.nodes])
                min_z,min_y,min_x = nodes_list[0]
                tuple_coor = ((min_z,haut),(min_y,lar),(min_x,long))
                if long >= lar and long >= haut:
                    return _sous_recur(graph,tuple_coor,2,density)
                if lar >= long and lar >= haut:
                    return _sous_recur(graph,tuple_coor,1,density)
                else:
                    return _sous_recur(graph,tuple_coor,0,density)
        
        self.graph = _recur_maze(self.graph,(self.height,self.length,self.width),self.density)

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
    maze = Maze(4,4,4)
    plot_interactive_3d(maze)