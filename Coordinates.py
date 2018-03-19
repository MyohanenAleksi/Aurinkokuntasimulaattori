
class Coordinates(object):
    """Coordinates for the celestial object in the system"""

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_z(self):
        return self.z
    def set_x(self,x):
        self.x = x
    def set_y(self,y):
        self.y = y
    def set_z(self,z):
        self.z = z
