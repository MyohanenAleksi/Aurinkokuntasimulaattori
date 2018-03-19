
from System import System
from SystemFileError import *
from celestialbody import CelestialBody
import math


class InitConditionReader(object):
    """This class reads the inital conditions of a system from a setup file and adds all planets and moons to the system"""

    def load_initial_condition(self,input):
        
        current_line= ''
        try:
            current_line = input.readline()
            header_parts = current_line.split(":")

            if header_parts[0].strip(" ") != "SOLARSYSTEM":
                raise SystemFileError("Invalid file type")
            if header_parts[1].strip().lower() != "initialconditionfile":
                raise SystemFileError("Invalid file type")
            current_line = input.readline()
            header_parts = current_line.split(":")
            if header_parts[0].strip(" ").lower() == "#system":
                self.system = System(header_parts[1].strip(" "),1*math.pow(float(header_parts[2]),float(header_parts[3])))
            else:
                raise SystemFileError("No System Information")
            while current_line != '':
                current_line = input.readline()
                if current_line.strip().lower() == "#newobject":
                    info_line = input.readline().strip(" ")
                    flag_fix = False
                    while info_line[0] != "#":
                        parts = info_line.split(":")
                        try:
                            if parts[0].strip(" ").lower() == "name":
                                name = parts[1].strip(" ")
                        except IndexError:
                            raise SystemFileError("Insufficient information")
                        try:    
                            if parts[0].strip(" ").lower() == "fixed":
                               flag_fix = True
                        except IndexError:
                            raise SystemFileError("Invalid information")
                        try:
                            if parts[0].strip(" ").lower() == "mass":
                                mass = float(parts[1].strip(" ").lower())*math.pow(10,float(parts[2].strip(" ").lower()))
                        except IndexError:
                            raise SystemFileError("Insufficient information")
                        try:
                            if parts[0].strip(" ").lower()  == "velocity_x":
                                vx = float(parts[1].strip(" ").lower())*math.pow(10,float(parts[2].strip(" ").lower()))
                        except IndexError:
                            raise SystemFileError("Insufficient information")
                        try:
                            if parts[0].strip(" ").lower()  == "velocity_y":
                                vy = float(parts[1].strip(" ").lower())*math.pow(10,float(parts[2].strip(" ").lower()))
                        except IndexError:
                            raise SystemFileError("Insufficient information")
                        try:
                            if parts[0].strip(" ").lower()  == "velocity_z":
                                vz = float(parts[1].strip(" ").lower())*math.pow(10,float(parts[2].strip(" ").lower()))
                        except IndexError:
                            raise SystemFileError("Insufficient information")
                        try:
                            if parts[0].strip(" ").lower()  == "coordinate_x":
                                coord_x = float(parts[1].strip(" ").lower())*math.pow(10,float(parts[2].strip(" ").lower()))
                        except IndexError:
                            raise SystemFileError("Insufficient information")
                        try:
                            if parts[0].strip(" ").lower()  == "coordinate_y":
                                coord_y = float(parts[1].strip(" ").lower())*math.pow(10,float(parts[2].strip(" ").lower()))
                        except IndexError:
                            raise SystemFileError("Insufficient information")
                        try:
                            if parts[0].strip(" ").lower()  == "coordinate_z":
                                coord_z = float(parts[1].strip(" ").lower())*math.pow(10,float(parts[2].strip(" ").lower()))
                        except IndexError:
                            raise SystemFileError("Insufficient information")
                        try:
                            if parts[0].strip(" ").lower()  == "radius":
                                radius = float(parts[1].strip(" ").lower())*math.pow(10,float(parts[2].strip(" ").lower()))
                        except IndexError:
                            raise SystemFileError("Insufficient information")
                        try:
                            if parts[0].strip(" ").lower() == "color":
                                color1 = float(parts[1])
                                color2 = float(parts[2])
                                color3 = float(parts[3])
                        except IndexError:
                            raise SystemFileError("Insufficient information")
                        
                        info_line = input.readline().strip(" ")
                    try:
                        body = CelestialBody(name,mass)
                    except Exception:
                        raise SystemFileError("Invalid Name or Mass")
                    if flag_fix == True:
                        body.set_fixed()
                    else:
                        body.set_unfixed()
                    try:
                        body.set_location(coord_x,coord_y,coord_z)
                    except Exception:
                        raise SystemFileError("Invalid Coordinates")
                    try:
                        body.set_velocity(vx,vy,vz)
                    except Exception:
                        raise SystemFileError("Invalid Velocity")
                    try:
                        body.set_radius(radius)
                    except Exception:
                        raise SystemFileError("Invalid radius")
                    try:
                        body.set_color(color1,color2,color3)
                    except Exception:
                        raise SystemFileError("Invalid Color")
                    self.system.add_body(body)
                    del vx, vy, vz
                    del coord_x, coord_y, coord_z
                    del name ,mass, radius
                    del color1, color2, color3
            return self.system
        except OSError:
            raise SystemFileError("Reading initial condition failed")
        