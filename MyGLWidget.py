import numpy
import math
import MyConst

from initreader import *
from BodyGraphicsItem import BodyGraphicsItem
from PyQt5 import _QOpenGLFunctions_4_1_Core
from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt, QTimer, QRect
from PyQt5.QtGui import QColor, QSurfaceFormat, QOpenGLVersionProfile, QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import *
from OpenGL import GLU, GL, GLUT


class myGLWidget(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)
    
    def __init__(self,parent = None):
        super(myGLWidget,self).__init__(parent)
        self.system = None
        self.has_system = False
        
        self.zoom = -50
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.dy = 0
        self.dx = 0
        self.GraphicItems =[]
        self.objects = []
        self.lastpos = QPoint()
        self.black = QColor.fromCmykF(1.0, 1.0, 1.0, 0.0)
           
           
    
    def set_System(self,system,filename):
        self.system = system
        self.system_file = filename
        self.scaling = self.system.scaling
        self.has_system = True
        self.updateBodies()
        self.update()

    def minimumSizeHint(self):
        return QSize(50,50)

    def sizeHint(self):
        return QSize(800,600)
    
    def setXRotation(self,angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self,angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self,angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()
    
    def setXTraverse(self,step):
        "Function for moving around WiP"
        self.dx += step
        self.update()

    def setYTraverse(self, step):
        "Function for moving around WiP"
        self.dy += step
        self.update()
    
    def set_simulation_speed(self,value):
        "sets the simulation speed according to the slider value"
        if value == 2:
            coef = 0.2
        elif value == 1:
            coef = 0.5
        elif value == 0:
            coef = 1
        elif value == -1:
            coef = 2
        elif value == -2:
            coef = 5
        return coef*10 # default speed is 10 ms 

    def normalizeAngle(self,angle):
        while angle< 0:
            angle += 360*16
        while angle>360*16:
            angle -= 360*16
        return angle
   
    
    def initializeGL(self):
        
        self.C = self.context()
        f = QSurfaceFormat()
        q = QOpenGLVersionProfile(f)
        self.gl = self.C.versionFunctions(q)
        self.setClearColor(self.black)
        if self.has_system:
            self.updateBodies()
            self.updateObjects(self.GraphicItems)
        self.gl.glShadeModel(self.gl.GL_FLAT)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glEnable(self.gl.GL_CULL_FACE)
       
        
    def paintGL(self):
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glLoadIdentity()
        self.gl.glTranslated(self.dx, self.dy, self.zoom)
        self.gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        self.gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        self.gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        
        self.updateObjects(self.GraphicItems)

    def resizeGL(self,width,height):
        side = min(width,height)
        if side < 0:
            return
        self.gl.glViewport((width-side)//2,(height-side)//2,side,side)
        self.gl.glMatrixMode(self.gl.GL_PROJECTION)
        self.gl.glLoadIdentity()
        self.gl.glFrustum(-30, +30, -30, +30, 30, 100.0)
        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)
        
    
    def mousePressEvent(self, event):
        self.lastpos = event.pos()
        
    
    def wheelEvent(self, event):
        "Mousewheel controls the zoom"
        numDegrees = event.angleDelta() / 8
        numSteps = (numDegrees/15)
        if numSteps.y() < 0:
            self.zoom += -0.5
        elif numSteps.y() > 0:
            self.zoom += 0.5
        self.update()
            
    def keyPressEvent(self, event):
        "Function for moving around. Work in Progress"
        if event.buttons() & Qt.LeftArrow:
            self.setXTraverse(-0.5)
        if event.buttons() & Qt.RightArrow:
            self.setXTraverse(0.5)
        if event.buttons() & Qt.UpArrow:
            self.setYTraverse(0.5)
        if event.buttons() & Qt.DownArrow:
            self.setYTraverse(-0.5)
    
    def mouseMoveEvent(self, event):
        "Handling the rotation with mouse. Click and drag"
        dx = event.x() - self.lastpos.x()
        dy = event.y() - self.lastpos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8*dy)
            self.setYRotation(self.yRot +8*dx)
        
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot+ 8*dy)
            self.setZRotation(self.zRot+ 8*dx)
        self.lastpos = event.pos()    

   
    def updateObjects(self,bodies):
        "Called within the paintgl function to draw all the objects"
      
        for item in bodies:
            self.drawOrb(item.radius,item.x,item.y,item.z,item.color)
            print(item.name,str(10*math.sqrt(math.pow(item.x,2)+math.pow(item.y,2)+math.pow(item.z,2)))+" Mkm,", str(item.velocity)+" m/s,",str(item.acceleration)+ " m/s2,")# prints the distance to the origin,
                                                                                                # which is by default the location of the central star

    
    def drawOrb(self,radius,center_x,center_y,center_z,color):
        "draws a sphere with given radius and location"
       
        quad = GLU.GLUquadric()
        quad = GLU.gluNewQuadric()
        self.setColor(color)
        self.gl.glTranslated(center_x,center_y,center_z)
        GLU.gluQuadricOrientation(quad, GLU.GLU_OUTSIDE)
        GLU.gluSphere(quad,radius,60,60)
        self.gl.glTranslated(-center_x,-center_y,-center_z)
       

    def setClearColor(self, c):
        self.gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self,c):
        self.gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def Simulate(self):
        "Calls the system class simulate function to advance the simulation. This function is controlled by a timer"
        self.system.simulate()
        self.updateBodies()
        self.update()

    def updateBodies(self):
        "Retrieves the information about the objects in the system for drawing"
        self.GraphicItems = []
        bodies = self.system.get_objects()
        for item in bodies:
            body = BodyGraphicsItem(item.get_name(),self.scaling*item.location.get_x(),self.scaling*item.location.get_y(),self.scaling*item.location.get_z(),item.radius,item.velocity.get_length(),item.acceleration.get_length())
            body.color(QColor.fromCmykF(item.color1, item.color2, item.color3, 0.0))
            self.GraphicItems.append(body)
    
    def set_timer(self,slider):
        self.speed_control = slider
        self.timer_speed = self.speed_control.value()
        self.timer = QTimer()
        self.start = False
        self.timer.timeout.connect(self.Simulate)
        
    def start_timer(self):
        speed = self.set_simulation_speed(self.speed_control.value())
        self.timer.start(speed) 
            
    def start_stop(self):
        "Connected to the start/stop button. Switches the timer to the opposite state ie. from on to off and vice versa"
        if self.has_system:

            if self.start != True:
                self.start = True
            elif self.start == True:
                self.start = False
            if self.start == True:
                self.start_timer() # speed of the simulation
            elif self.start == False:
                self.timer.stop()
        
    def reset(self):
        "reads the last InitialConditionFile again to reset the simulation"
        file = open(self.system_file,"r")
        reader = InitConditionReader()
        self.system = reader.load_initial_condition(file)
        file.close()
        self.updateBodies()
        self.updateObjects(self.GraphicItems)
       
        self.zoom = -50
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.dy = 0
        self.dx = 0
        self.update()

