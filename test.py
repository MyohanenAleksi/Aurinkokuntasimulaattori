import math
import unittest
from io import StringIO
from satellite import Satellite
from System import System
from SystemFileError import *
from Coordinates import Coordinates
from celestialbody import CelestialBody
from initreader import InitConditionReader

class Test(unittest.TestCase):
    """ Tests for the solar system simulation"""
    def setUp(self):
        self.InitReader = InitConditionReader()

    def test_given_condition(self):

        self.input_file = StringIO()
        self.input_file.write("SOLARSYSTEM: InitialCOndition\n ")
        self.input_file.write("#System: Sun&Earth:10:-10\n\n")
        self.input_file.write("#newObject\n name:Sun\n mass: 1.989:30\n")
        self.input_file.write("coordinate_x: 0:0\n coordinate_y : 0:0 \n coordinate_z:0:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z:0:0 \n radius:0:0 \n")
        self.input_file.write("#NewObject \n name: Earth \n mass : 5.974:24 \n radius:0:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z : 0:0 \n")
        self.input_file.write("coordinate_x:149.59787:9 \n coordinate_y :0:0 \n coordinate_z:0:0\n")

        self.input_file.seek(0,0)

        system = self.InitReader.load_initial_condition(self.input_file)

        self.input_file.close()

        self.assertEqual("Sun&Earth", system.name, "Wrong system name")


    def test_wrong_file_type(self):

        self.input_file = StringIO()
        self.input_file.write("BASESYSTEM: InitialCondition\n ")
        self.input_file.write("#System: Sun&Earth:10:-10\n\n")
        self.input_file.write("#newObject\n name:Sun\n mass: 1.989:30\n")
        self.input_file.write("coordinate_x: 0:0\n coordinate_y : 0:0 \n coordinate_z:0:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z:0:0 \n radius:0:0 \n")
        self.input_file.write("#NewObject \n name: Earth \n mass : 5.974:24 \n radius:0:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z : 0:0 \n")
        self.input_file.write("coordinate_x:149.59787:9 \n coordinate_y :0:0 \n coordinate_z:0:0\n")

        self.input_file.seek(0,0)
        system_error_raised = None
        try:
            system = self.InitReader.load_initial_condition(self.input_file)
        except SystemFileError as error:
            system_error_raised = error
        self.input_file.close()
        self.assertNotEqual(None, system_error_raised, "SystemFileError wasn't raised")

    def test_missing_exponent(self):
        "Testing missing exponent on Earth's velocity_y"
        self.input_file = StringIO()
        self.input_file.write("SOLARSYSTEM: InitialCondition\n ")
        self.input_file.write("#System: Sun&Earth:10:-10\n\n")
        self.input_file.write("#newObject\n name:Sun\n mass: 1.989:30\n")
        self.input_file.write("coordinate_x: 0:0\n coordinate_y : 0:0 \n coordinate_z:0:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z:0:0 \n radius:1:0 \n color:0:0:1\n #" )
        self.input_file.write("#NewObject \n name: Earth \n mass : 5.974:24 \n radius:0.1:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:29300 \n velocity_z : 0:0 \n")
        self.input_file.write("coordinate_x:149.59787:9 \n coordinate_y :0:0 \n coordinate_z:0:0\n")
        self.input_file.write("color:1:0:0 \n#")
        
        self.input_file.seek(0,0)

        check = None

        try:
            system = self.InitReader.load_initial_condition(self.input_file)
        except SystemFileError as error:
            check = error
        self.assertNotEqual(None,check,"SystemFileError wasn't raised")

    def test_missing_mass(self):
        self.input_file = StringIO()
        self.input_file.write("SOLARSYSTEM: InitialCondition\n ")
        self.input_file.write("#System: Sun&Earth:10:-10\n\n")
        self.input_file.write("#newObject\n name:Sun\n mass: 1.989:30\n")
        self.input_file.write("coordinate_x: 0:0\n coordinate_y : 0:0 \n coordinate_z:0:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z:0:0 \n radius:1:0 \n color:0:0:1\n #" )
        self.input_file.write("#NewObject \n name: Earth \n\n radius:0.1:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:29300 \n velocity_z : 0:0 \n")
        self.input_file.write("coordinate_x:149.59787:9 \n coordinate_y :0:0 \n coordinate_z:0:0\n")
        self.input_file.write("color:1:0:0 \n#")
        self.input_file.seek(0,0)
        
        check = None

        try:
            system = self.InitReader.load_initial_condition(self.input_file)
        except SystemFileError as error:
            check = error
        self.assertNotEqual(None,check,"SystemFileError wasn't raised")

    def test_missing_name(self):
        self.input_file = StringIO()
        self.input_file.write("SOLARSYSTEM: InitialCondition\n ")
        self.input_file.write("#System: Sun&Earth:10:-10\n\n")
        self.input_file.write("#newObject\n name:Sun\n mass: 1.989:30\n")
        self.input_file.write("coordinate_x: 0:0\n coordinate_y : 0:0 \n coordinate_z:0:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z:0:0 \n radius:1:0 \n color:0:0:1\n #" )
        self.input_file.write("#NewObject \n\n mass : 5.974:24 \n radius:0.1:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:29300 \n velocity_z : 0:0 \n")
        self.input_file.write("coordinate_x:149.59787:9 \n coordinate_y :0:0 \n coordinate_z:0:0\n")
        self.input_file.write("color:1:0:0 \n#")
        self.input_file.seek(0,0)
        
        check = None

        try:
            system = self.InitReader.load_initial_condition(self.input_file)
        except SystemFileError as error:
            check = error
        self.assertNotEqual(None,check,"SystemFileError wasn't raised")

    def test_missing_coordinate(self):
        self.input_file = StringIO()
        self.input_file.write("SOLARSYSTEM: InitialCondition\n ")
        self.input_file.write("#System: Sun&Earth:10:-10\n\n")
        self.input_file.write("#newObject\n name:Sun\n mass: 1.989:30\n")
        self.input_file.write("coordinate_x: 0:0\n coordinate_y : 0:0 \n coordinate_z:0:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z:0:0 \n radius:1:0 \n color:0:0:1\n #" )
        self.input_file.write("#NewObject \n name: Earth \n mass : 5.974:24 \n radius:0.1:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:29300 \n velocity_z : 0:0 \n")
        self.input_file.write("coordinate_x:149.59787:9 \n \n coordinate_z:0:0\n")
        self.input_file.write("color:1:0:0 \n#")
        self.input_file.seek(0,0)
        
        check = None

        try:
            system = self.InitReader.load_initial_condition(self.input_file)
        except SystemFileError as error:
            check = error
        self.assertNotEqual(None,check,"SystemFileError wasn't raised")

    def test_missing_velocity(self):
        self.input_file = StringIO()
        self.input_file.write("SOLARSYSTEM: InitialCondition\n ")
        self.input_file.write("#System: Sun&Earth:10:-10\n\n")
        self.input_file.write("#newObject\n name:Sun\n mass: 1.989:30\n")
        self.input_file.write("coordinate_x: 0:0\n coordinate_y : 0:0 \n coordinate_z:0:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z:0:0 \n radius:1:0 \n color:0:0:1\n #" )
        self.input_file.write("#NewObject \n name: Earth \n mass : 5.974:24 \n radius:0.1:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:29300 \n \n")
        self.input_file.write("coordinate_x:149.59787:9 \n coordinate_y:0:0\n coordinate_z:0:0\n")
        self.input_file.write("color:1:0:0 \n#")
        self.input_file.seek(0,0)
        
        check = None

        try:
            system = self.InitReader.load_initial_condition(self.input_file)
        except SystemFileError as error:
            check = error
        self.assertNotEqual(None,check,"SystemFileError wasn't raised")

        
    def test_missing_color(self):
        self.input_file = StringIO()
        self.input_file.write("SOLARSYSTEM: InitialCondition\n ")
        self.input_file.write("#System: Sun&Earth:10:-10\n\n")
        self.input_file.write("#newObject\n name:Sun\n mass: 1.989:30\n")
        self.input_file.write("coordinate_x: 0:0\n coordinate_y : 0:0 \n coordinate_z:0:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z:0:0 \n radius:1:0 \n color:0:0:1\n #" )
        self.input_file.write("#NewObject \n name: Earth \n mass : 5.974:24 \n radius:0.1:0 \n")
        self.input_file.write("velocity_x:0:0 \n velocity_y:29300 \n velocity_:0:0\n")
        self.input_file.write("coordinate_x:149.59787:9 \n coordinate_y:0:0\n coordinate_z:0:0\n")
        self.input_file.write("\n#")
        self.input_file.seek(0,0)
        
        check = None

        try:
            system = self.InitReader.load_initial_condition(self.input_file)
        except SystemFileError as error:
            check = error
        self.assertNotEqual(None,check,"SystemFileError wasn't raised")

        def test_missing_system_information(self):
            self.input_file = StringIO()
            self.input_file.write("SOLARSYSTEM: InitialCondition\n ")
            self.input_file.write("#System: Sun&Earth\n\n")
            self.input_file.write("#newObject\n name:Sun\n mass: 1.989:30\n")
            self.input_file.write("coordinate_x: 0:0\n coordinate_y : 0:0 \n coordinate_z:0:0 \n")
            self.input_file.write("velocity_x:0:0 \n velocity_y:0:0 \n velocity_z:0:0 \n radius:1:0 \n color:0:0:1\n #" )
            self.input_file.write("#NewObject \n name: Earth \n mass : 5.974:24 \n radius:0.1:0 \n")
            self.input_file.write("velocity_x:0:0 \n velocity_y:29300 \n velocity_:0:0\n")
            self.input_file.write("coordinate_x:149.59787:9 \n coordinate_y:0:0\n coordinate_z:0:0\n")
            self.input_file.write("color:1:0:0\n#")
            self.input_file.seek(0,0)
        
            check = None

            try:
                system = self.InitReader.load_initial_condition(self.input_file)
            except SystemFileError as error:
                check = error
            self.assertNotEqual(None,check,"SystemFileError wasn't raised")


if __name__ == "__main__":
    unittest.main()
