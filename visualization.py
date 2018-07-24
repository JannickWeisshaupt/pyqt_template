# -*- coding: utf-8 -*-

import os

os.environ['ETS_TOOLKIT'] = 'qt4'

from pyface.qt import QtGui, QtCore


import numpy as np
import matplotlib as mpl

mpl.use('Qt4Agg')


mpl.rc('font', **{'size': 22})

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random

from pyface.api import GUI
from traits.api import HasTraits, Instance, on_trait_change, Range, Bool, Button, Array, Float, Enum
from traitsui.api import View, Item, Group, HGroup

from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
    SceneEditor
from mayavi.core.api import Engine, PipelineBase, Source



class MatplotlibExample(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.first_plot_bool = True
        # a figure instance to plot on
        self.figure = plt.figure(1)
        plt.close(plt.figure(1))
        self.ax = None
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        color = self.palette().color(QtGui.QPalette.Base)
        self.figure.patch.set_facecolor([color.red() / 255, color.green() / 255, color.blue() / 255])

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        option_widget = QtGui.QWidget()
        option_widget.setFixedHeight(60)
        option_layout = QtGui.QHBoxLayout(option_widget)
        option_layout.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(option_widget)

        width_text = 70
        width_label = 40
        from main import EntryWithLabel
        self.xmin_entry = EntryWithLabel(option_widget, 'xmin', width_text=width_text, width_label=width_label)
        self.xmin_entry.connect_editFinished(self.plot)
        option_layout.addWidget(self.xmin_entry)
        self.xmax_entry = EntryWithLabel(option_widget, 'xmax', width_text=width_text, width_label=width_label)
        self.xmax_entry.connect_editFinished(self.plot)
        option_layout.addWidget(self.xmax_entry)

        self.setLayout(layout)
        self.show()

    def plot(self):

        if self.first_plot_bool:
            self.ax = self.figure.add_subplot(111)
        else:
            self.ax.cla()

        x = np.linspace(0,1,1000)
        y = np.random.randn(1000,1)
        self.ax.plot(x,y)

        try:
            xmin = float(self.xmin_entry.get_text())
        except Exception:
            xmin = None

        try:
            xmax = float(self.xmax_entry.get_text())
        except Exception:
            xmax = None

        if xmin is not None:
            self.ax.set_xlim(left=xmin)
        if xmax is not None:
            self.ax.set_xlim(right=xmax)


        if self.first_plot_bool:
            self.first_plot_bool = False
            self.figure.tight_layout()
        self.canvas.draw()
        print('plot is updated')

    def update_tab(self):
        self.plot()


class MayaviExample(HasTraits):
    n_balls = Range(1, 400, 50, mode='spinner')  # )
    black_balls = Bool(True)


    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=450, width=500, show_label=False),
                Group('_', 'n_balls', 'black_balls', orientation='horizontal'),
                resizable=True,  # We need this to resize with the parent widget
                )

    scene = Instance(MlabSceneModel, ())

    def __init__(self,):
        super().__init__()

    @on_trait_change('scene.activated,n_balls,black_balls')
    def update_plot(self, *args, **kwargs):
        # We can do normal mlab calls on the embedded scene.
        self.scene.mlab.clf(figure=self.scene.mayavi_scene)
        data = np.random.randn(self.n_balls, 3)
        if self.black_balls:
            color = (0.3,0.3,0.3)
        else:
            color = (1,0,0)
        pts = self.scene.mlab.points3d(data[:,0],data[:,1],data[:,2], figure=self.scene.mayavi_scene,color=color)

