
import pd3
from pd3.proto.study_pb2 import IMMOBILE
import matplotlib.pyplot as plt
import ipyvolume as ipv
import numpy as np
import matplotlib.cm as cm
from matplotlib import colors as mcolors
from matplotlib.collections import LineCollection
from matplotlib import collections as mc
import seaborn as sns
import pylab as pl
import importlib
import Graph_class
importlib.reload(Graph_class)
from Graph_class import Graph

def normalize(a, b, c):
    """Creates a unit vector from a, b, c"""
    vector = np.array([a, b, c])
    return vector / np.linalg.norm(vector)

def convert_line_to_coordinates(line):
    """! \brief Converts data in line into x,y,z coordinates
    
    Goes through the line array and collects the x, y, and z values needed to plot the line segments
    \param Takes in an array of node information (x, y, z)
    Returns: x, y, z, xs, ys, and zs which are points to plot on the graph
    """
    xs = []
    ys = []
    zs = []
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
    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)
    
    return xs, ys, zs, x, y, z

                
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

def plot_study3D(study, timestep = 0, do_scatter=False, color_scheme = "tab10"):
    """! \brief Plots the dislocation system in 3D at the given timestep.

    Plots a given dislocation system with orthogonal axes.
    \param study Self instance.
    \param timestep The timestep to plot.
    \param do_scatter Whether to plot dislocation nodes or not.
    """
   
    colors = []
    lines = []
    
    #creating the graph
    proto_graph = study.export_protobuf()
    g = Graph(proto_graph, timestep, color_scheme)
    
    #collect the information to plot
    g.dfs(lines, colors)
    lines = np.array(lines)
    
    #segmenting data for the plot
    segments_list = []
    fig = ipv.figure()
    for line, color in zip(lines, colors):
        xs, ys, zs, x, y, z = convert_line_to_coordinates(line)
        ipv.pylab.plot(x, y, z, color = color)    
   
    #draw dots
    if do_scatter:
        scatter = ipv.scatter(xs, ys, zs)
    ipv.show()


def plot_study(study, timestep = 0, x_axis=(1, 0, 0), y_axis=(0, 1, 0), color_scheme = "tab10"):
    
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

    color = []
    lines = []
    #creating the graph
    proto_graph = study.export_protobuf()
    g = Graph(proto_graph, timestep, color_scheme)
    
    #collect the information to plot
    g.dfs(lines, color)
    lines = np.array(lines)
    
    #segmenting data for the plot
    segments_list = []
    for line in lines:
        xs, ys, zs, x, y, z = convert_line_to_coordinates(line)
        segments = list(zip(xs,ys))
        segments_list.append(segments)
        
    #Plot
    line_segments = LineCollection(segments_list, colors = color, linestyle='solid')
    fig, ax = pl.subplots()
    ax.add_collection(line_segments)
    ax.autoscale()
    ax.margins(0.1)
    plt.title("Plot Study")
    plt.xlabel("x")
    plt.ylabel("y")
