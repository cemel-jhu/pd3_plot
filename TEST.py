import pd3
from pd3.proto.study_pb2 import IMMOBILE
import matplotlib.pyplot as plt
import ipyvolume as ipv
import numpy as np
import matplotlib.cm as cm
from matplotlib.collections import LineCollection
from matplotlib import collections as mc
import seaborn as sns
import pylab as pl
import importlib
import Graph
importlib.reload(Graph)
from Graph import Graph


class Plotter:
    # constructor
    def __init__(self, protobuf):
        self.protobuf = protobuf

    def normalize(self, a, b, c):
        """Creates a unit vector from a, b, c"""
        vector = np.array([a, b, c])
        return vector / np.linalg.norm(vector)

    def convert_line_to_coordinates(self, line):
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

    def is_normal(self, x_axis, y_axis):
        """! \brief Tests wether the given vectors are normal 

        Test the given vectors to find out if they are normal and ensures that the two axises are orthogonal
        \param x and y axis

        Return: whether or not the axis are normal
        """
        normal = True
        if x_axis.dot(y_axis) != 0:
            normal = False
        return normal

    def plot_3D(self,
                timestep=0,
                do_scatter=False,
                color_scheme="tab10",
                num_colors=13):
        """! \brief Plots the dislocation system in 3D at the given timestep.

        \param timestep The timestep to plot.
        \param do_scatter Whether to plot dislocation nodes or not.
        \param color_scheme The color_scheme that the user wants the lines to be colored with 

        """

        colors = []
        lines = []

        #creating the graph
        g = Graph(self.protobuf, timestep, color_scheme, num_colors)

        #collect the information to plot
        g.dfs(lines, colors)
        lines = np.array(lines)

        #segmenting data for the plot
        segments_list = []
        fig = ipv.figure()
        for line, color in zip(lines, colors):
            xs, ys, zs, x, y, z = self.convert_line_to_coordinates(line)
            ipv.pylab.plot(x, y, z, color=color, size=5, connected=True, visible_markers=True, marker = 'diamond')

        #draw dots
        if do_scatter:
            scatter = ipv.scatter(xs, ys, zs)
        ipv.show()

    def plot_2D(self,
                timestep=0,
                x_axis=(1, 0, 0),
                y_axis=(0, 1, 0),
                color_scheme="tab10",
                num_colors=13):
        """! \brief Plots the dislocation system at the given timestep.

        Plots a given dislocation system with orthogonal axes.
        \param x_axis The x axis to project the system on.
        \param y_axis The y axis to projec the system on.
        \param timestep The timestep to plot.
        \param color_scheme The color_scheme that the user wants the lines to be colored with 
        """
        
        self.normalize(*x_axis)
        self.normalize(*y_axis)
        
        x_axis = np.array(x_axis)
        x_axis = x_axis / np.linalg.norm(x_axis)
        y_axis = np.array(y_axis)
        y_axis = y_axis / np.linalg.norm(y_axis)

        if self.is_normal(x_axis, y_axis) == False:
            raise pd3.Pd3Exception("Provided axes are not normal.")

        color = []
        lines = []
        #creating the graph
        g = Graph(self.protobuf, timestep, color_scheme, num_colors)

        #collect the information to plot
        g.dfs(lines, color)
        lines = np.array(lines)

        #segmenting data for the plot
        segments_list = []
        for line in lines:
            xs, ys, zs, x, y, z = self.convert_line_to_coordinates(line)
            segments = list(zip(xs, ys))
            segments_list.append(segments)

        #Plot
        line_segments = LineCollection(segments_list,
                                       colors=color,
                                       linestyle='solid', linewidth = 1.5)
        fig, ax = pl.subplots()
        ax.add_collection(line_segments)
        ax.autoscale()
        ax.margins(0.1)
        plt.title("Plot Study")
        plt.xlabel("x")
        plt.ylabel("y")

    def movie_3D(self,
                 timestep_start=0,
                 timestep_end=42,
                 step=10,
                 do_scatter=False,
                 color_scheme="tab10",
                 num_colors=13):
        """! \brief Plots the dislocation system in 3D over a small period of time.

        \param timestep_start The start time for plotting the dislocations
        \param timestep_end The end time for plotting dislocations
        \param step The interval of how often the dislocations are plotted over the specified period of time
        \param do_scatter Whether to plot dislocation nodes or not.
        \param color_scheme The color_scheme that the user wants the lines to be colored with 

        """ 
        s = []
#         ipv.pylab.figure()
        times = []
        while timestep_start < timestep_end:
            times.append(timestep_start)
            timestep_start = timestep_start + step
        print("Timestep 1")
        turn = 0
        x = []
        y = []
        z = []
        xs = []
        ys = []
        zs = []
#         fig = []
        lines = []
        colors = []
        time = times[0]
        #timestep loop
        fig = ipv.pylab.figure(key = 1)
        ipv.pylab.figure(key = 1)
        x.append(float("nan"))
        y.append(float("nan"))
        z.append(float("nan"))

        g = Graph(self.protobuf, time, color_scheme, num_colors)

        #collect the information to plot
        g.dfs(lines, colors)
#             lines = np.array(lines)

        #segmenting data for the plot
        segments_list = []

#             lines = np.array(lines)
#             print(lines)
        for array in lines:

            for line in array:
#                     print (line)
                x.append(line[0])
                y.append(line[1])
                z.append(line[2]) 
            x.append(float("nan"))
            y.append(float("nan"))
            z.append(float("nan"))
        xs = np.array(x)
        ys = np.array(y)
        zs = np.array(z)
        ipv.scatter(xs, ys, zs, marker='sphere', size=0, connected=True)
        
#         print("Timestep 2")
#         time = times[1]
#         #second turn
#         turn2 = 0
        
# #         time = time + step
#         x2 = []
#         y2 = []
#         z2 = []
#         xs2 = []
#         ys2 = []
#         zs2 = []
#         s2 = []
# #         lines2 = []
# #         colors2= []
#         #second time step loop
# #         fig2 = ipv.pylab.figure(key = time)
#         ipv.pylab.figure(key = 1)
#         x2.append(float("nan"))
#         y2.append(float("nan"))
#         z2.append(float("nan"))

#         g = Graph(self.protobuf, time, color_scheme, num_colors)

#         #collect the information to plot
#         g.dfs(lines, colors)
# #             lines = np.array(lines)

#         #segmenting data for the plot
# #         segments_list = []

# #             lines = np.array(lines)
# #             print(lines)
#         for array in lines:

#             for line in array:
# #                     print (line)
#                 x2.append(line[0])
#                 y2.append(line[1])
#                 z2.append(line[2]) 
#             x2.append(float("nan"))
#             y2.append(float("nan"))
#             z2.append(float("nan"))
#         xs2 = np.array(x2)
#         ys2 = np.array(y2)
#         zs2 = np.array(z2)
#         ipv.scatter(xs2, ys2, zs2, marker='sphere', size=0, connected=True)

#         ipv.animation_control(fig.scatters, sequence_length = 200, interval = 1000)
        print("Show")
        ipv.show()

    def movie_2D(self,
                 x_axis=(1, 0, 0),
                 y_axis=(0, 1, 0),
                 timestep_start=0,
                 timestep_end=42,
                 step=10,
                 do_scatter=False,
                 color_scheme="tab10",
                 num_colors=13):
        """! \brief Plots the dislocation system at the given timestep.

        Plots a given dislocation system with orthogonal axes.
        \param x_axis The x axis to project the system on.
        \param y_axis The y axis to projec the system on.
        \param timestep The timestep to plot.
        \param color_scheme The color_scheme that the user wants the lines to be colored with 
        """
        self.normalize(*x_axis)
        self.normalize(*y_axis)
        
        x_axis = np.array(x_axis)
        x_axis = x_axis / np.linalg.norm(x_axis)
        y_axis = np.array(y_axis)
        y_axis = y_axis / np.linalg.norm(y_axis)

        if self.is_normal(x_axis, y_axis) == False:
            raise pd3.Pd3Exception("Provided axes are not normal.")

        times = []
        while timestep_start < timestep_end:
            times.append(timestep_start)
            timestep_start = timestep_start + step

        #creating the graph
        
        for time in times:
            timestep = time
            color = []
            lines = []
            g = Graph(self.protobuf, timestep, color_scheme, num_colors)

            #collect the information to plot
            g.dfs(lines, color)
            lines = np.array(lines)

            #segmenting data for the plot
            segments_list = []
            for line in lines:
                xs, ys, zs, x, y, z = self.convert_line_to_coordinates(line)
                segments = list(zip(xs, ys))
                segments_list.append(segments)

            #Plot
            line_segments = LineCollection(segments_list,
                                           colors=color,
                                           linestyle='solid')
            fig, ax = pl.subplots()
            ax.add_collection(line_segments)
            ax.autoscale()
            ax.margins(0.1)
            plt.title("Plot Study")
            plt.xlabel("x")
            plt.ylabel("y")
