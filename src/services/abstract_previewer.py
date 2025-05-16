##
# Created by @taps on Friday, 16 May 2025.
##

import PySide6.QtCore as Core
import PySide6.QtWidgets as Widgets
import PySide6.QtGui as Gui


class AbstractPreviewer(Core.QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

    def available(self) -> bool:
        """
        Determine whether this previewer can play files.

        Returns:
            bool: 
        """
        raise NotImplementedError()

    def play(self, fileName: str):
        """
        This function must be asynchronous, i.e. it must return
        immediately without waiting for the player to exit.

        Args:
            fileName (str): 
        """
        raise NotImplementedError()

    def playPortion(self, fileName: str, startPos: int, endPos: int):
        """
        Play a portion of the file from @a t_begin to @a t_end (seconds).

        Args:
            fileName (str): 
            startPos (int): 
            endPos (int): 
        """
        pass

    def playFrom(self, fileName: str, startPos: int):
        raise NotImplementedError()

    def playUntil(self, fileName: str, endPos: int):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()