
import math
import MyConst
from vector import vector
from Coordinates import Coordinates

class CelestialBody(object):
    """This class represents the objects in a stellar system of class System"""
    def __init__(self, name, mass):
        self.set_name(name)
        self.set_mass(mass) # Constant
        self.set_color(0.4,0.0,0.0)  # default color is green
        self.location = Coordinates(0,0,0)
        self.fixed = False
        self.velocity = vector(0,0,0)
        self.acceleration = vector(0,0,0)
        self.system = None
        

    def set_name(self,name):
        self.name = str(name)
    def set_mass(self,mass):
        self.mass = float(mass)
    
    def set_radius(self,radius):
        self.radius = radius

    def set_system(self,system):
        """ sets the system of the object"""
        self.system = system
        return True
    def set_color(self,color1,color2,color3):
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
    def set_fixed(self):
        self.fixed = True
    def set_unfixed(self):
        self.fixed = False
    
    def get_name(self):
        return self.name

    def calculate_acceleration(self):
        """ Calculates the acceleration caused by other objects in the system with their gravitational "pull" """
        if self.fixed != True:
            objects = self.system.get_objects() 
            # temporal variables for the new acceleration vector
            ax = 0
            ay = 0
            az = 0          
            for item in objects:
                if item.name != self.name:
                    distance = self.calculate_distance(item) 
                    unit_x = (item.location.get_x()-self.location.get_x())/distance
                    unit_y = (item.location.get_y()-self.location.get_y())/distance
                    unit_z = (item.location.get_z()-self.location.get_z())/distance
                    ax = ax + MyConst.G*item.mass*math.pow(distance,-2)*unit_x
                    ay = ay + MyConst.G*item.mass*math.pow(distance,-2)*unit_y
                    az = az + MyConst.G*item.mass*math.pow(distance,-2)*unit_z
            self.acceleration.set_x(ax) 
            self.acceleration.set_y(ay)
            self.acceleration.set_z(az)    
            self.acceleration.set_length()           
        

    def calculate_distance(self,object):
        """ Returns the distance between self and another object"""
        dist_x = abs(self.location.get_x() - object.location.get_x())
        dist_y = abs(self.location.get_y() - object.location.get_y())
        dist_z = abs(self.location.get_z() - object.location.get_z())
        return math.sqrt(math.pow(dist_x,2)+math.pow(dist_y,2)+math.pow(dist_z,2))
    
    def set_velocity(self,x,y,z):
        """ Sets the velocity vector of the body"""
        self.velocity.set_x(x)
        self.velocity.set_y(y)
        self.velocity.set_z(z)
        self.velocity.set_length()

    def update_velocity(self):
        """ Calculates the change to the velocity caused by acceleration"""
        if self.fixed != True:
            new_x = self.velocity.get_x() + self.acceleration.get_x()*MyConst.Time_step
            new_y = self.velocity.get_y() + self.acceleration.get_y()*MyConst.Time_step
            new_z = self.velocity.get_z() + self.acceleration.get_z()*MyConst.Time_step
            self.set_velocity(new_x,new_y,new_z)

    def set_location(self,x,y,z):
        """ Sets the location of the body"""
        self.location.set_x(x)
        self.location.set_y(y)
        self.location.set_z(z)

    def move(self):
        """ Calculates the new location for the body where it moves within time time_step 
        with its velocity and acceleration at that time instant. The unit for time_step is seconds"""
        if self.fixed != True:
            x = self.location.get_x()
            y = self.location.get_y()
            z = self.location.get_z()
            new_x = x + self.velocity.get_x()*MyConst.Time_step + 0.5*self.acceleration.get_x()*math.pow(MyConst.Time_step,2)
            new_y = y + self.velocity.get_y()*MyConst.Time_step + 0.5*self.acceleration.get_y()*math.pow(MyConst.Time_step,2)
            new_z = z + self.velocity.get_z()*MyConst.Time_step + 0.5*self.acceleration.get_z()*math.pow(MyConst.Time_step,2)
            self.set_location(new_x,new_y,new_z)
        