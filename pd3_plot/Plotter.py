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
from Graph import Graph
import os, sys


class Plotter:
    def __init__(self, protobuf):
        self.protobuf = protobuf

    def normalize(self, a, b, c):
        """Creates a unit vector from a, b, c"""
        vector = np.array([a, b, c])
        return vector / np.linalg.norm(vector)

    def convert_line_to_coordinates(self, line):
        """! \brief Converts data in line into x, y, z coordinates

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
        """! \brief Tests whether the given vectors are normal.

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
                num_colors=13,
                do_vr=False):
        """! \brief Plots the dislocation system in 3D at the given timestep.

        \param timestep The timestep to plot
        \param do_scatter Whether to plot dislocation nodes or not
        \param color_scheme The color_scheme that the user wants the lines to be colored with
        \param num_colors The number of colors in the given color_scheme
        \param do_vr Whether to save the link for using VR or not

        """

        colors = []
        lines = []

        # Creating the graph
        g = Graph(self.protobuf, timestep, color_scheme, num_colors)

        # Collect the information to plot
        g.dfs(lines, colors)
        lines = np.array(lines)

        # Segmenting data for the plot
        fig = ipv.figure()
        for line, color in zip(lines, colors):
            xs, ys, zs, x, y, z = self.convert_line_to_coordinates(line)
            ipv.pylab.plot(x,
                           y,
                           z,
                           color=color,
                           size=5,
                           connected=True,
                           visible_markers=True,
                           marker='diamond')

        # Draw dots
        if do_scatter:
            scatter = ipv.scatter(xs, ys, zs)

        # Save the figure for VR
        if do_vr:
            ipv.save("Plotter_VR.html")

        ipv.show()

    def plot_2D(self,
                timestep=0,
                x_axis=(1, 0, 0),
                y_axis=(0, 1, 0),
                color_scheme="tab10",
                num_colors=13):
        """! \brief Plots the dislocation system at the given timestep.

        Plots a given dislocation system with orthogonal axes.
        \param timestep The timestep to plot.
        \param x_axis The x axis to project the system on.
        \param y_axis The y axis to projec the system on.
        \param color_scheme The color_scheme that the user wants the lines to be colored with
        """

        x_axis = self.normalize(*x_axis)
        y_axis = self.normalize(*y_axis)

        if self.is_normal(x_axis, y_axis) == False:
            raise pd3.Pd3Exception("Provided axes are not normal.")

        color = []
        lines = []

        # Creating the graph
        g = Graph(self.protobuf, timestep, color_scheme, num_colors)

        # Collect the information to plot
        g.dfs(lines, color)
        lines = np.array(lines)

        # Segmenting data for the plot
        segments_list = []
        for line in lines:
            xs, ys, zs, x, y, z = self.convert_line_to_coordinates(line)
            points = list(zip(xs, ys, zs))
            segments_x = np.dot(points, x_axis)
            segments_y = np.dot(points, y_axis)
            segments = list(zip(segments_x, segments_y))
            segments_list.append(segments)

        # Plot
        line_segments = LineCollection(segments_list,
                                       colors=color,
                                       linestyle='solid',
                                       linewidth=1.5)
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
        \param num_colors The number of colors in the color_scheme

        """
        times = []
        while timestep_start < timestep_end:
            times.append(timestep_start)
            timestep_start = timestep_start + step

        # Creating the graph
        for time in times:
            timestep = time
            colors = []
            lines = []
            g = Graph(self.protobuf, timestep, color_scheme, num_colors)

            # Collect the information to plot
            g.dfs(lines, colors)
            lines = np.array(lines)

            # Segmenting data for the plot
            segments_list = []
            fig = ipv.figure()
            for line, color in zip(lines, colors):
                xs, ys, zs, x, y, z = self.convert_line_to_coordinates(line)
                ipv.pylab.plot(x, y, z, color=color)

            # Draw dots
            if do_scatter:
                scatter = ipv.scatter(xs, ys, zs)
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
        \param timestep_start The start time for plotting the dislocations
        \param timestep_end The end time for plotting dislocations
        \param step The interval of how often the dislocations are plotted over the specified period of time
        \param do_scatter Whether to plot dislocation nodes or not.
        \param color_scheme The color_scheme that the user wants the lines to be colored with
        \param num_colors The number of colors in the color_scheme
        """
        x_axis = self.normalize(*x_axis)
        y_axis = self.normalize(*y_axis)

        if self.is_normal(x_axis, y_axis) == False:
            raise pd3.Pd3Exception("Provided axes are not normal.")

        times = []
        while timestep_start < timestep_end:
            times.append(timestep_start)
            timestep_start = timestep_start + step

        # Ceating the graph
        for time in times:
            timestep = time
            color = []
            lines = []
            g = Graph(self.protobuf, timestep, color_scheme, num_colors)

            # Collect the information to plot
            g.dfs(lines, color)
            lines = np.array(lines)

            # Segmenting data for the plot
            segments_list = []
            for line in lines:
                xs, ys, zs, x, y, z = self.convert_line_to_coordinates(line)
                segments = list(zip(xs, ys))
                segments_list.append(segments)

            # Plot
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

    def vr_link(self, *args, **kwargs):
        kwargs["do_vr"] = True
        self.plot_3D(*args, **kwargs)
        print(
            "Here is the link to view the model in VR: " + "\n" +
            "http://10.160.48.168:8000/user/reap2020/view/notebooks/pd3_plot/Plotter_VR.html"
        )
