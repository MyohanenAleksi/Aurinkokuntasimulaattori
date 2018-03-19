import numpy
import math
import MyConst

from initreader import *
from BodyGraphicsItem import BodyGraphicsItem
from PyQt5 import _QOpenGLFunctions_4_1_Core
from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt, QTimer, QRect
from PyQt5.QtGui import QColor, QSurfaceFormat, QOpenGLVersionProfile, QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import *
from MyGLWidget import myGLWidget
class GUI(QWidget):
    """description of class"""
   
    def __init__(self):
        super(GUI,self).__init__()
        self.glwidget = myGLWidget()
        self.slider = self.createSlider()
        self.GraphicItems = []
        mainlayout = QHBoxLayout() 
        vert = QVBoxLayout()
        grid = QGridLayout()
        slider = self.createSlider()
        sim_button = self.sim_button()
        reset_button  = self.reset_button()
        #add_button = self.add_satellite_button()     
        menu_bar = self.createMenu()
        vert.addWidget(menu_bar)
        vert.addWidget(self.glwidget)
        self.glwidget.set_timer(slider)
        grid.addWidget(sim_button,1,2)
        #grid.addWidget(add_button,2,2) # Button for adding a satellite. Feature not yet included
        grid.addWidget(reset_button,2,2)
        mainlayout.addLayout(vert)
        mainlayout.addWidget(slider)
        mainlayout.addLayout(grid)
        self.setLayout(mainlayout)   
        self.setWindowTitle("Solar System Simulator")
        
   
     
    def minimumSizeHint(self):
        return QSize(50,50)

    def sizeHint(self):
        return QSize(800,600)
    
    
    def createMenu(self):
        menu_bar = QMenuBar()
        menu_bar.setMaximumHeight(30)
        
        filemenu = menu_bar.addMenu("File")
        load_action = QAction("Load System",self)
        exit_action = QAction("Exit",self)
        exit_action.triggered.connect(exit)
        load_action.triggered.connect(self.findDialog)
        filemenu.addAction(load_action)
        filemenu.addSeparator()
        filemenu.addAction(exit_action)
        return menu_bar

    def findDialog(self):
        
        filename = QFileDialog.getOpenFileName(self,"Open Data File","Initial_Condition_Files","*.txt")
        print(filename)
        if not filename[0] == '':
            [system,system_file] = self.read_system_file(filename)
            self.glwidget.set_System(system,system_file)
        
    def read_system_file(self,filename):
        "Assembles the filename from the directory path and loads the system"
        dir = filename[0]
        
        parts = dir.split("/")
        name = parts[len(parts)-2] + "/" + parts[len(parts)-1]
   
        file = open(name,"r")
        reader = InitConditionReader()
        system =  reader.load_initial_condition(file)
        file.close()
        return system, name

    def createSlider(self):
        slider = QSlider(Qt.Vertical)
        slider.setRange(-2, 2)
        slider.setSingleStep(1)
        slider.setPageStep(1)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksRight)
        slider.setSliderPosition(0)
        return slider

    def reset_button(self):
        button = QPushButton()
        button.setText("Reset")
        button.pressed.connect(self.glwidget.reset)
        return button

    def sim_button(self):
        button = QPushButton()
        button.setText("Start/Stop")
        button.pressed.connect(self.glwidget.start_stop)
        return button

    def add_satellite_button(self):
        button = QPushButton()
        button.setText("Add satellite")
        button.pressed.connect
        return button
    def set_System(self,system):
        self.system = system
    def set_Scaling(self,scaling):
        self.scaling = scaling

    
       