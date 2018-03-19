import sys
from PyQt5.QtWidgets import QApplication
from GUI import GUI, myGLWidget
import numpy
from System import *
from celestialbody import *
from Coordinates import *
from initreader import *
import math

def main():
   
    global app
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    
    
    sys.exit(app.exec_())
    
  
if __name__ == '__main__':
    main()