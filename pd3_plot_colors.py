import pd3
from pd3.proto.study_pb2 import IMMOBILE
import matplotlib.pyplot as plt
import ipyvolume as ipv
import numpy as np
import matplotlib.cm as cm
from matplotlib import colors as mcolors
from matplotlib.collections import LineCollection
from matplotlib import collections as mc
import pylab as pl


def normalize(a, b, c):
    """Creates a unit vector from a, b, c"""
    vector = np.array([a, b, c])
    return vector / np.linalg.norm(vector)


def create_graph(study, timestep, x_axis, y_axis, not_visited, node_vectors, node_vectors_2d, links):
    """! \brief Creates a graph
    
    Exports a graph from protobuf, and gets the edge and node information
    \param Takes in a graph
    \param Takes in x_axis and y_axis for plotting
    \param Takes in a set which represents the nodes that have been visited
    \param Takes in 2 lookup for node_id to to node_vector.
    """
        
    graph = study.export_protobuf()
    vertices = graph.state[timestep].nodes
    edges = graph.state[timestep].links
    g = {}
#     links = { 
#        node_a: { node_b: segment_info } }
#     node
   
    for edge in edges:
        not_visited.add(edge.leading)
        not_visited.add(edge.trailing)
        leading_neighbors = g.get(edge.leading, [])
        leading_neighbors.append(edge.trailing)
        trailing_neighbors = g.get(edge.trailing, [])
        trailing_neighbors.append(edge.leading)
        g[edge.leading] = leading_neighbors
        g[edge.trailing] = trailing_neighbors

    for edge in edges: # (1, 2)
        if edge.leading not in links:
            links[edge.leading] = {}

        if edge.trailing not in links:
            links[edge.trailing] = {}

        links[edge.leading][edge.trailing] = edge.slip
        links[edge.trailing][edge.leading] = edge.slip

    for node_id in vertices:
        node = vertices[node_id]
        node_3d = np.array([node.x, node.y, node.z])
        node_vectors[node_id] = node_3d
        
        node_x = x_axis.dot(node_3d)
        node_y = y_axis.dot(node_3d)
        node_vectors_2d[node_id] = (node_x, node_y)

    return g

def collect_and_plot(lines):
    """! \brief Collects data for lines and plots 
    
    Goes through the lines array and collects the x, y, and z values needed to plot and then plots those values
    \param Takes in an array of node information (x, y, z)
    
    Returns: xs, ys, and zs which are points to plot on the graph
    """
    
    lines = np.array(lines)
    length = len(lines)
    fig = ipv.figure()
    for line in lines:
        x = []
        y = []
        z = []
        for array in line:
            x.append(array[0])
            y.append(array[1])
            z.append(array[2])
        xs += x
        ys += y
        zs += z
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        ipv.pylab.plot(x, y, z, color = 'blue')
    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)
    
    return xs, ys, zs, x, y, zs

def dfs(graph, node_vectors, not_visited, visited, links, color):
    """! \brief Searches graph.
    
    Search the provided graph using depth first search, returns a bunch of lines.
    \param Takes in hashmap representing graph.
    \param Takes in a lookup for node_id to to node_vector.
    \param Takes in a set representing not_visited nodes
    \param Takes in an empty set representing nodes that have already been visited
    
    Returns: Lines, which is a bunch of lines we can plot
    """
    lines = []
    color = []
    color_lookup = {0: "red", 1: "blue"}
    
    def search(graph, node_vectors, current, previous, line, links, previous_slip, color):
        neighbors = graph[current]
        here = node_vectors[current]
        branch = line
        branch.append(here)

        first_visit = current not in visited
        end_of_line = (len(neighbors) == 1 and neighbors[0] == previous)

        visited.add(current)
        if current in not_visited:
            not_visited.remove(current)

        if not first_visit or end_of_line:
            lines.append(branch)
            color.append(color_lookup[previous_slip])
            return

        first_iteration = True
        for node in neighbors:
            slip = links[current][node]
            if slip != previous_slip:
                # What a hack!
                # See if you can find a nicer way of doing this
                if first_iteration:
                    lines.append(branch)
                    color.append(color_lookup[previous_slip])
                branch = [here]
                    
            if node != previous:
                search(graph, node_vectors, node, here, branch, links, slip, color)
                branch = [here]
            first_iteration = False
                
    while len(not_visited) > 0:
        start_node = not_visited.pop()
        search(graph, node_vectors, start_node, None, [], links, None, color)
        
    return lines, color         
                
def is_normal(x_axis, y_axis):
    """! \brief Tests wether the given vectors are normal 

    Test the given vectors to find out if they are normal and ensures that the two axises are orthogonal
    \param x and y axis
    
    Return: whether or not the axis are normal
    """
    normal = True
    if x_axis.dot(y_axis) != 0:
        normal = False
    return normal

def plot_study3D(study, timestep = 0, do_scatter=False):
    """! \brief Plots the dislocation system in 3D at the given timestep.

    Plots a given dislocation system with orthogonal axes.
    \param study Self instance.
    \param timestep The timestep to plot.
    \param do_scatter Whether to plot dislocation nodes or not.
    """

    not_visited = set()
    visited = set()
    node_vectors = {}
    node_vectors_2d = {}
    links = {}
    colors = []
    #create the graph
    g = create_graph(
        study, timestep, x_axis, y_axis, not_visited, node_vectors,
        node_vectors_2d, links)  

    print(links)
    
    #collect plotting informatoin
    lines, colors = dfs(g, node_vectors_2d, not_visited, visited, links, colors)
    
    xs = []
    ys = []
    zs = []    
    #organize plotting information and draw lines
    xs, ys, zs = collect_data(lines)
    
    #draw dots
    if do_scatter:
        scatter = ipv.scatter(xs, ys, zs)
    ipv.show()


def plot_study(study, timestep = 0, x_axis=(1, 0, 0), y_axis=(0, 1, 0)):
    """! \brief Plots the dislocation system at the given timestep.

    Plots a given dislocation system with orthogonal axes.
    \param study Self instance.
    \param x_axis The x axis to project the system on.
    \param y_axis The y axis to projec the system on.
    \param timestep The timestep to plot.
    """
    x_axis = np.array(x_axis)
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.array(y_axis)
    y_axis = y_axis / np.linalg.norm(y_axis)
    
    if is_normal(x_axis, y_axis) == False:
        raise pd3.Pd3Exception("Provided axes are not normal.")

    not_visited = set()
    visited = set()
    node_vectors = {}
    node_vectors_2d = {}
    links = {}
#   print(links)
    color = []
    #creating the graph
    g = create_graph(study, timestep, x_axis, y_axis, not_visited, node_vectors, node_vectors_2d, links) 
    
    #collect the information to plot
    lines, color = dfs(g, node_vectors_2d, not_visited, visited, links, color)
#     print(lines)
#     print()
    
    
#     for slip in colors:# go through colors and comapre the slip, if it equals each other, they get the same color if its different, it gets a different color

#     print(links)
#     print(color)
    # Plots lines
    # print(color)
    """
    final_colors = []
    previous_slip = 0
    for slip in color:
        if slip == color[previous_slip]:
            #slip.color = 'blue'
            final_colors += slip
            previous_slip = slip
        else:
            #slip.color = 'red'
            final_colors += slip
            previous_slip = slip
    """
    # replace color_lookup with this
    # colors = [mcolors.to_rgba(c)
    #       for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]

    # Just this
    #colors = []
    #color_scheme = plt.rcParams['axes.prop_cycle'].by_key()['color']
    #for c in color_scheme:
    #    colors.append(mcolors.to_rgba(c))
    
    # assert len(color) == len(lines)
    
    line_segments = LineCollection(lines, linestyle='solid')
#     lc = mc.LineCollection(lines, colors = color)
    fig, ax = pl.subplots()
#     ax.add_collection(lc)
    ax.add_collection(line_segments)
    ax.autoscale()
    ax.margins(0.1)
    plt.title("Plot Study")
    plt.xlabel("x")
    plt.ylabel("y")
