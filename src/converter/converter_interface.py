##
# Created by @taps on Wednesday, 02 April 2025.
##

from PySide6.QtCore import QObject, QProcess, Signal

from src.converter.conversion_parameters import ConversionParameters


class ConverterInterface(QObject):
    progressRefreshed = Signal(float)

    def __init__(self, parent=None):
        super(ConverterInterface, self).__init__(parent)

    def executableName(self) -> str:
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()

    def processReadChannel(self) -> QProcess.ProcessChannel:
        raise NotImplementedError()

    def fillParameterList(self, param: ConversionParameters, lst: list, needs_audio_filter: bool):
        """
        Fill parameter list and determine whether the configuration needs
        additional audio filtering. This function must be called before
        starting the process. Implementations of this function should
        do necessary setup, such as obtaining stream duration for calculating
        progress.
        :param param: [in] the conversion parameter
        :param lst: [out] the command-line parameter list
        :param needs_audio_filter: [out] whether AudioFilter should be used. The return value is true implies that the parameter list makes the conversion process wait for data input from stdin.
        :return:
        """
        raise NotImplementedError()

    def parseProcessOutput(self, line: str):
        raise NotImplementedError()

    def progress(self) -> float:
        raise NotImplementedError()

    def errorMessage(self) -> str:
        return ''
