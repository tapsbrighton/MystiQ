##
# Created by @taps on Friday, 16 May 2025.
##

import PySide6.QtCore as Core
import PySide6.QtWidgets as Widgets
import PySide6.QtGui as Gui

class XmlLookupTable:
    """
    Read an xml file and provide path lookup syntax.
    """
    
    def __init__(self):
        pass
    
    def readFile(self, file:Core.QIODevice)->bool:
        """
        Read xml from file.
        Existing data are cleared no matter the function succeeds or fails.

        Args:
            file (Core.QIODevice): a QIODevice opened for reading

        Returns:
            bool: true if succeed, false if failed
        """
        pass
    
    def readString(self, text: str)->bool:
        """
        Read xml from string
        Existing data are cleared no matter the function succeeds or fails.

        Args:
            text (str): a string to read from

        Returns:
            bool: true if succeed, false if failed
        """
        pass
    
    def setPrefix(self, path: str):
        """
        Set the lookup prefix.
        
        The lookup prefix will be prepended to the path in each lookup.
        Setting the prefix can prevent repeatly typing common prefixes.

        Args:
            path (str): the path to be prepended
        """
        pass
    
    def prefix(self)->str:
        """
        get the current prefix

        Returns:
            str: 
        """
        pass
    
    def lookup(self, path: str)->tuple[bool, str]:
        """
        Find the data associated with path.

        Args:
            path (str): the path to lookup. Note that the prefix will be prepended
            to this path. The path is similar to unix file paths but without leading
            or trailing '/'. For example: level1/level2/level3

        Returns:
            tuple[bool, str]: the data associated with the path.
        """
        pass
    
    def attribute(self, path: str, attr: str)->str:
        """
        Get the value of the attribute associated with @a path

        Args:
            path (str): the path to the node
            attr (str): name of the attribute

        Returns:
            str: 
        """
        pass
    
    def clear(self):
        """
        Clear all xml data.
        """
        pass