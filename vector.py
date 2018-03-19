
import math

class vector(object):
    """Similar class to the Coordinates except this represents a 3 dimensional vector that points from one coordinates to another.
    """ 
    def __init__(self,x,y,z):
        """The x, y and z are the vector's coordinate components"""
        
        self.x = x
        self.y = y
        self.z = z
        self.set_length()
    def set_x(self,x):
        self.x= x
    def set_y(self,y):
        self.y = y
    def set_z(self,z):
        self.z = z
           
    def set_length(self):
        """ Calculates the total lenght of the vector from its components"""
        self.length = math.sqrt(math.pow(self.x,2)+math.pow(self.y,2)+math.pow(self.z,2))

    def get_length(self):
        """ Returns the lenght of the vector """
        return self.length

    def inverse(self):
        """ Inverses the vector direction"""
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
    def get_x(self):
        """ Returns the x coordinate component"""
        return self.x
    def get_y(self):
        """ Returns the y coordinate component"""
        return self.y
    def get_z(self):
        """ Returns the z coordinate component"""
        return self.z
   

