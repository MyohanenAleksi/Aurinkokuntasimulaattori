import MyConst


class System(object):
    """description of class"""
    """ The system in which the simulation happens. The class keeps track of every object that exists in
    system during simulation"""
    def __init__(self, name,scaling):
        self.name = name
        self.Objects = []
        self.scaling = scaling

        

    def get_objects(self):
        """ returns the objects in this system"""
        return self.Objects
    
    def get_body(self,name):
        """ Return a single body which has a name Name or false if no body of that name exists in the system"""
        objects = self.get_objects()
        print(name)
        for item in objects:
            item_name = item.get_name()
            print(item_name)
            if item_name.strip(" ").lower() == name.strip(" ").lower():
                print("Found")  
                return item
        
        

    def add_body(self, body):
        if body.set_system(self):
            self.Objects.append(body)
    
    def remove_body(self, body):
        """ Only satellites may be removed"""
        raise NotImplementedError
    
    def update_body_accelerations(self):
        """ Calculates  the acceleration caused by gravity for each body in the system"""
        for item in self.Objects:
            item.calculate_acceleration()
    
    def update_body_velocity(self):
        """ Calculates  the acceleration caused by gravity for each body in the system"""
        for item in self.Objects:
            item.update_velocity()


    def update_body_positions(self):
        """ Updates the positions of all the bodies in the system"""
        for item in self.Objects:
            item.move()

    def simulate(self):
        """Calculates the simulation constants.time_step seconds forward"""
        self.update_body_accelerations()
        self.update_body_positions()
        self.update_body_velocity()


