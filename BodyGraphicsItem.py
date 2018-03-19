
from PyQt5 import QtWidgets, QtGui, QtCore
class BodyGraphicsItem(object):
    """Contains information on how to draw a specific body"""

    def __init__(self,name ,center_x,center_y,center_z, radius,velocity, acceleration):
        self.set_radius(radius)
        self.x = center_x
        self.y = center_y
        self.z = center_z
        self.name = name
        self.velocity = velocity # just a pure value opposed to the vector class in celestialbody. Used for printing information
        self.acceleration = acceleration 

    def set_radius(self,radius):
        self.radius = radius

    def color(self,Qcolor):
        self.color = Qcolor    

