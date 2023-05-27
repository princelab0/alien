from paradox.NWENV import *
from qtpy.QtWidgets import QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QTextEdit,QColorDialog,QFontDialog
from qtpy.QtGui import QImage, QPixmap, QFont
from qtpy.QtCore import Signal, QSize, QTimer
import os
from paradox.extension.biopython.mol import PDBVisualizer

# load csv file widgets
class ChooseFileInputWidget(IWB, QPushButton):
    
    path_chosen = Signal(str)

    def __init__(self, params):
        IWB.__init__(self, params)
        QPushButton.__init__(self, "Select")

        self.clicked.connect(self.button_clicked)

    def button_clicked(self):
        file_path = QFileDialog.getOpenFileName(self, 'Select CSV file')[0]
        try:
            file_path = os.path.relpath(file_path)
        except ValueError:
            return
        
        self.path_chosen.emit(file_path)

# widgets for the folder selection
class ChooseFolderInputWidget(IWB, QPushButton):
    
    path_chosen = Signal(str)

    def __init__(self, params):
        IWB.__init__(self, params)
        QPushButton.__init__(self, "Select")

        self.clicked.connect(self.button_clicked)

    def button_clicked(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Train folder')[0]
        try:
            folder_path = os.path.relpath(folder_path)
        except ValueError:
            return
        
        self.path_chosen.emit(folder_path)

class ButtonNode_MainWidget(QPushButton, MWB):

    def __init__(self, params):
        MWB.__init__(self, params)
        QPushButton.__init__(self)

        self.clicked.connect(self.update_node)


# widgets for the color selection
class ChooseColorInputWidget(IWB, QPushButton):
    
    path_chosen = Signal(str)

    def __init__(self, params):
        IWB.__init__(self, params)
        QPushButton.__init__(self, "Select")

        self.clicked.connect(self.button_clicked)

    def button_clicked(self):
        folder_path = QColorDialog.getColor()
        print("Your color value is ...")
        print(folder_path.name())
        
        self.path_chosen.emit(folder_path.name())

# widgets for the color selection
class ChooseFontInputWidget(IWB, QPushButton):
    
    path_chosen = Signal(str)

    def __init__(self, params):
        IWB.__init__(self, params)
        QPushButton.__init__(self, "Select")

        self.clicked.connect(self.button_clicked)

    def button_clicked(self):
        folder_path = QFontDialog.getFont()
        print("Your color value is ...")
        print(folder_path)

        
        self.path_chosen.emit(folder_path)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


# Exporting the widgets class
export_widgets(
    ChooseFileInputWidget,
    ChooseFolderInputWidget,
    ButtonNode_MainWidget,
    ChooseColorInputWidget,
    ChooseFontInputWidget,

)        