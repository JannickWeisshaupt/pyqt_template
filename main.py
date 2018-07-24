import sys
if not sys.getfilesystemencoding():
    sys.getfilesystemencoding = lambda: 'UTF-8'
import os

os.environ['ETS_TOOLKIT'] = 'qt4'

import imp

try:
    imp.find_module('PySide')  # test if PySide if available
except ImportError:
    os.environ['QT_API'] = 'pyqt'  # signal to pyface that PyQt4 should be used

from pyface.qt import QtGui, QtCore

if os.path.exists(__file__+'/DEBUG'):
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



class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show()

        self.main_widget = QtGui.QWidget(parent=self)

        self.error_dialog = QtGui.QErrorMessage(parent=self)
        self.error_dialog.resize(700, 600)
        # error dialog can be used with self.error_dialog.showMessage(string)

        self.layout = QtGui.QVBoxLayout(self.main_widget)

        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.currentChanged.connect(self.tab_is_changed)
        self.layout.addWidget(self.tabWidget)

        self.button_widget = SomeButtonWidget(self)
        self.button_widget2 = SomeButtonWidget(self)

        self.tabWidget.addTab(self.button_widget,'Some Buttons')
        self.tabWidget.addTab(self.button_widget2,'More Buttons')


        # self.setWindowTitle("Marcel codet")
        # self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setMinimumSize(700, 700)
        self.resize(1000, 900)
        self.setCentralWidget(self.main_widget)

        self.show()

    def closeEvent(self, event):
        if not DEBUG:
            reply = QtGui.QMessageBox.question(self, 'Message',
                                               "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if DEBUG or reply == QtGui.QMessageBox.Yes:
            app.quit()
            sys.exit()

    def tab_is_changed(self, i):
        print('tab {} is selected'.format(i))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()

    app.exec_()