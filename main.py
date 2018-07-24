import sys
if not sys.getfilesystemencoding():
    sys.getfilesystemencoding = lambda: 'UTF-8'
import os

import numpy as np


os.environ['ETS_TOOLKIT'] = 'qt4'

import imp

try:
    imp.find_module('PySide')  # test if PySide if available
except ImportError:
    os.environ['QT_API'] = 'pyqt'  # signal to pyface that PyQt4 should be used


from pyface.qt import QtGui, QtCore
from visualization import MatplotlibExample,MayaviExample



if os.path.exists(__file__+'/DEBUG'): # if there is a file DEBUG in the main folder the program will run in debug mode
    DEBUG = True
else:
    DEBUG = False


class EntryWithLabel(QtGui.QWidget):
    def __init__(self, parent, label, value=None, width_text=200, width_label=90,tooltip=None):
        QtGui.QWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.layout = QtGui.QHBoxLayout(self)
        self.textbox = QtGui.QLineEdit(self)
        if width_text:
            self.textbox.setMaximumWidth(width_text)
        self.label_widget = QtGui.QLabel(label, parent=self)
        if width_label:
            self.label_widget.setMaximumWidth(width_label)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.label_widget)
        self.layout.addWidget(self.textbox)
        self.editFinished_command = None

        if value is not None:
            self.textbox.setText(value)

        if tooltip is not None:
            self.textbox.setToolTip(tooltip)

    def get_text(self):
        return self.textbox.text()

    def set_text(self, text):
        self.textbox.setText(text)

    def connect_editFinished(self, command):
        self.editFinished_command = command
        self.textbox.editingFinished.connect(self.handleEditingFinished)

    def handleEditingFinished(self):
        if self.textbox.isModified():
            self.editFinished_command()
        self.textbox.setModified(False)


class LabeledLabel(QtGui.QWidget):
    def __init__(self,label,value='',width_label=None):
        super(LabeledLabel,self).__init__()
        self.layout = QtGui.QHBoxLayout(self)
        self.label_label = QtGui.QLabel(text=label)
        self.label_label.setAlignment(QtCore.Qt.AlignLeft)
        if width_label:
            self.label_label.setFixedWidth(width_label)
        self.layout.addWidget(self.label_label)
        self.value_label = QtGui.QLabel(text=value)
        self.value_label.setAlignment(QtCore.Qt.AlignLeft)
        self.value_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.layout.addWidget(self.value_label)

    def text(self,value):
        self.value_label.setText(value)

    def change_label(self,label):
        self.label_label.setText(label)


class SomeButtonWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        layout = QtGui.QHBoxLayout(self)
        self.buttons = []
        for i in range(5):
            button = QtGui.QPushButton('{}'.format(i))
            button.clicked.connect(self.click_event)
            button.setFixedHeight(50)
            layout.addWidget(button)

    def click_event(self):
        print('button was clicked')

    def update_tab(self):
        print('buttons are updated, which means nothing is done')

class MayaviQWidget(QtGui.QWidget):
    def __init__(self, visualization,parent=None):
        super().__init__(parent=parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.visualization = visualization
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)

    def update_tab(self):
        self.visualization.update_plot()

class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show()

        self.main_widget = QtGui.QWidget(parent=self)

        self.error_dialog = QtGui.QErrorMessage(parent=self)
        self.error_dialog.resize(700, 600)
        # error dialog can be used with self.error_dialog.showMessage(string)

        self.layout = QtGui.QVBoxLayout(self.main_widget) # QVBoxLayout is a vertical layout.
        # use QHBoxLayout for horizontal layout

        self.tabWidget = QtGui.QTabWidget(self.main_widget)
        self.tabWidget.currentChanged.connect(self.tab_is_changed)
        self.layout.addWidget(self.tabWidget)

        self.button_widget = SomeButtonWidget(self)
        self.matplotlib_example = MatplotlibExample()
        mayavi_example = MayaviExample()
        self.mayavi_widget = MayaviQWidget(mayavi_example,parent=self)

        self.tabWidget.addTab(self.button_widget,'Some buttons')
        self.tabWidget.addTab(self.matplotlib_example,'matplotlib')
        self.tabWidget.addTab(self.mayavi_widget,'Mayavi')

        self.setWindowTitle("this is a template")
        # self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setMinimumSize(700, 700)
        self.resize(1000, 900)
        self.setCentralWidget(self.main_widget)

        self.plot_timer = QtCore.QTimer()
        self.plot_timer.timeout.connect(self.update_selected_tab)
        self.plot_timer.start(1000)

        self.show()

    def closeEvent(self, event):
        if not DEBUG:
            reply = QtGui.QMessageBox.question(self, 'Message',
                                               "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if DEBUG or reply == QtGui.QMessageBox.Yes:
            app.quit()
            sys.exit()

    def update_selected_tab(self):
        self.tabWidget.currentWidget().update_tab()

    def tab_is_changed(self, i):
        print('tab {} is selected'.format(i))


if __name__ == "__main__":
    app = QtGui.QApplication.instance() # Use this if mayavi is imported
    # app = QtGui.QApplication # use this if you don't import mayavi
    main = MainWindow()

    app.exec_()
