##
# Created by @taps on Friday, 16 May 2025.
##

import PySide6.QtCore as Core
import PySide6.QtWidgets as Widgets
import PySide6.QtGui as Gui

class Constants:
    @staticmethod
    def readFile(file: Core.QFile)->bool:
        pass
    
    @staticmethod
    def getBool(character: str)-> bool:
        pass
    
    @staticmethod
    def getInteger(character: str)->int:
        pass
    
    @staticmethod
    def getFloat(character: str)->float:
        pass
    
    @staticmethod
    def getSpaceSeparatedList(character: str)->list[str]:
        pass
    
    @staticmethod
    def getColor(character: str)->Gui.QColor:
        pass