
from celestialbody import CelestialBody

class Satellite(CelestialBody):
    """description of class"""
    
    def __init__(self, name, mass):
        super().__init__(self,name,mass)

    def use_engines(self):
        """ Satellite uses its engines to accelerate in the defined direction"""
        raise NotImplementedError

    