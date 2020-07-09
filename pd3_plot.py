import pd3
from pd3.proto.study_pb2 import IMMOBILE
import matplotlib.pyplot as plt
import ipyvolume as ipv
import numpy as np
import matplotlib.cm as cm
from matplotlib import collections as mc
import pylab as pl


def normalize(a, b, c):
    """Creates a unit vector from a, b, c"""
    vector = np.array([a, b, c])
    return vector / np.linalg.norm(vector)


def create_graph():
    """! \brief Creates a graph
    
    Exports a graph from protobuf, and gets the edge and node information
    \param 
    \param 
    """
    graph = study.export_protobuf()
    vertices = graph.state[timestep].nodes
    edges = graph.state[timestep].links
    g = {}
    not_visited = set()
    visited = set()
    
    for edge in edges:
        not_visited.add(edge.leading)
        not_visited.add(edge.trailing)
        leading_neighbors = g.get(edge.leading, [])
        leading_neighbors.append(edge.trailing)
        trailing_neighbors = g.get(edge.trailing, [])
        trailing_neighbors.append(edge.leading)
        g[edge.leading] = leading_neighbors
        g[edge.trailing] = trailing_neighbors

    node_vectors = {}
    for node_id in vertices:
        node = vertices[node_id]
        node_3d = np.array([node.x, node.y, node.z])
        node_vectors[node_id] = node_3d
    #3d    
        node_x = x_axis.dot(node_3d)
        node_y = y_axis.dot(node_3d)
        node_vectors[node_id] = (node_x, node_y)
    
def dfs(graph, node_vectors):
    """! \brief Searches graph.

    Search the provided graph usind depth first search, returns a bunch of lines.
    \param Takes in hashmap representing graph.
    \param Takes in a lookup for nod_id to to node_vector.
    
    Returns: Lines, which is a bunch of lines we can plot
    """


def plot_study3D(study, timestep = 0, do_scatter=False):
    """! \brief Plots the dislocation system in 3D at the given timestep.

    Plots a given dislocation system with orthogonal axes.
    \param study Self instance.
    \param timestep The timestep to plot.
    \param do_scatter Whether to plot dislocation nodes or not.
    """

    graph = study.export_protobuf()
    vertices = graph.state[timestep].nodes
    edges = graph.state[timestep].links
    g = {}
    not_visited = set()
    visited = set()
    
    for edge in edges:
        not_visited.add(edge.leading)
        not_visited.add(edge.trailing)
        leading_neighbors = g.get(edge.leading, [])
        leading_neighbors.append(edge.trailing)
        trailing_neighbors = g.get(edge.trailing, [])
        trailing_neighbors.append(edge.leading)
        g[edge.leading] = leading_neighbors
        g[edge.trailing] = trailing_neighbors

    node_vectors = {}
    for node_id in vertices:
        node = vertices[node_id]
        node_3d = np.array([node.x, node.y, node.z])
        node_vectors[node_id] = node_3d

    lines = []
    
    
    def dfs(current, previous, line, numberNode):
        neighbors = g[current]
        here = node_vectors[current]
        branch = line
        branch.append(here)
        # If this is our firt visit, then we should record this line.
        # Otherwise, we're in a loop!
        first_visit = current not in visited
        # This is the end of a dislocation line because:
        #       1) there's only 1 connection
        #       2) and that cpnnection is previous
        end_of_line = (len(neighbors) == 1 and neighbors[0] == previous)

        # Even if it's the end of the line, we try to add it to previous.
        visited.add(current)
        if current in not_visited:
            not_visited.remove(current)

        # Now we check to see if we should stop and record the line.
        if not first_visit or end_of_line:
            lines.append(branch)
            return

        for node in neighbors: #this starts the new branches?
            if node != previous:
                dfs(node, current, branch, 0)
                branch = [node_vectors[current]]
            
            
    while len(not_visited) > 0:
        start_node = not_visited.pop()
        dfs(start_node, 0, [], 0) 
    lines = np.array(lines)
    length = len(lines)
    fig = ipv.figure()
    xs = []
    ys = []
    zs = []
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
    if do_scatter:
        scatter = ipv.scatter(xs, ys, zs)

    ipv.show()


def plot_study(study, x_axis=(1, 0, 0), y_axis=(0, 1, 0), timestep = 0):
    """! \brief Plots the dislocation system at the given timestep.

    Plots a given dislocation system with orthogonal axes.
    \param study Self instance.
    \param x_axis The x axis to project the system on.
    \param y_axis The y axis to projec the system on.
    \param timestep The timestep to plot.
    """
    # Ensure x_axis, y_axis are normalized
    x_axis = np.array(x_axis)
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.array(y_axis)
    y_axis = y_axis / np.linalg.norm(y_axis)
    
    # https://numpy.org/doc/stable/
    if x_axis.dot(y_axis) != 0:
        raise pd3.Pd3Exception("Provided axes are not normal.")

    graph = study.export_protobuf()

    # Here's an example of how to break up our graph to get the edges and vertices.
    vertices = graph.state[timestep].nodes
    edges = graph.state[timestep].links
    g = {}
    not_visited = set()
    visited = set()
    
    for edge in edges:
        not_visited.add(edge.leading)
        not_visited.add(edge.trailing)
        leading_neighbors = g.get(edge.leading, [])
        leading_neighbors.append(edge.trailing)
        trailing_neighbors = g.get(edge.trailing, [])
        trailing_neighbors.append(edge.leading)
        g[edge.leading] = leading_neighbors
        g[edge.trailing] = trailing_neighbors

    node_vectors = {}
    for node_id in vertices:
        node = vertices[node_id]
        node_3d = np.array([node.x, node.y, node.z])
        node_x = x_axis.dot(node_3d)
        node_y = y_axis.dot(node_3d)
        node_vectors[node_id] = (node_x, node_y)
        
    
    # TODO: Find a way to reuse the DFS function
    lines = []
    def dfs(current, previous, line, numberNode):
        numberNode = len(visited) + 1
        if current in visited:
            if line: # if line != []
                lines.append(line)
            return
        visited.add(current) 
        if current in not_visited:
            not_visited.remove(current)
            
        here = node_vectors[current]
        #print(str(numberNode) + ") Line: " + str(line) + "    Curent: " + str(current))
        #print()
        
        #if you have to start a new branch, check the location and if it goes back, do not add to
        # line until you start going in the other direction?
        #everytime you have to go back to a different branch or direction, do not add to line until
        #you are at the point, and then at the end go back and fill the gap?
        
        branch = line
        branch.append(here)
        
        neighbors = g[current]
        for node in neighbors: #this starts the new branches?
            if node != previous:
                dfs(node, here, branch, 0)
                branch = [node_vectors[current]]
    
    while len(not_visited) > 0:
        start_node = not_visited.pop()
        dfs(start_node, None, [], 0)

    lc = mc.LineCollection(lines)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.title("Plot Study")
    plt.xlabel("x")
    plt.ylabel("y")
