##
# Created by @taps on Thursday, 03 April 2025.
##
import enum

from PySide6.QtCore import QProcess, Signal
from lowercase_booleans import false

from src.converter.conversion_parameters import ConversionParameters
from src.converter.converter_interface import ConverterInterface
from src.converter.exe_path import ExePath


class FFmpegInterface(ConverterInterface):
    progressRefreshed = Signal(float)

    def __init__(self, parent):
        super().__init__(parent)

    def executableName(self) -> str:
        pass

    def reset(self):
        pass

    def processReadChannel(self) -> QProcess.ProcessChannel:
        pass

    def needsAudioFiltering(self, param: ConversionParameters) -> bool:
        pass

    def fillParameterList(self, param: ConversionParameters, lst: list, needs_audio_filter: bool):
        pass

    def parseProcessOutput(self, data: str):
        pass

    def progress(self) -> float:
        pass

    def errorMessage(self) -> str:
        pass

    @staticmethod
    def getAudioEncoders(target: list) -> bool:
        pass

    @staticmethod
    def getVideoEncoders(target: list) -> bool:
        pass

    @staticmethod
    def getSubtitleEncoders(target: list) -> bool:
        pass

    @staticmethod
    def getFFmpegVersionInfo() -> str:
        pass

    @staticmethod
    def getFFmpegCodecInfo() -> str:
        pass

    @staticmethod
    def getFFmpegFormatInfo() -> str:
        pass

    @staticmethod
    def getSupportedMuxingFormats(target: set[str]) -> bool:
        pass

    @staticmethod
    def getSupportedDemuxingFormats(target: set[str]) -> bool:
        pass

    @staticmethod
    def hasFFmpeg():
        pass

    @staticmethod
    def refreshFFmpegInformation():
        pass


class Patterns:
    progress = "size=\\s*([0-9]+)kB\\s+time=\\s*([0-9]+\\.[0-9]+)\\s+bitrate=\\s*([0-9]+\\.[0-9]+)kbits/s"

    # another possible format where time is represented as hh:mm:ss
    progress2 = "size=\\s*([0-9]+)kB\\s+time=\\s*([0-9][0-9]):([0-9][0-9]):([0-9][0-9](\\.[0-9][0-9]?)?)\\s+bitrate=\\s*([0-9]+\\.[0-9]+)kbits/s"

    class Progress_1_Fields(enum.Enum):
        PROG_1_TIME = 2

    class Progress_2_Fields(enum.Enum):
        PROG_2_HR = 2
        PROG_2_MIN = 3
        PROG_2_SEC = 4

    duration = "Duration:\\s+([0-9][0-9]):([0-9][0-9]):([0-9][0-9](\\.[0-9][0-9]?)?)"


class Info:
    def __init__(self):
        self.is_encoders_read = 0
        self.ffmpeg_exist = false
        self.ffmpeg_version = ''
        self.ffmpeg_codec_info = ''
        self.ffmpeg_format_info = ''

        self.audio_encoders = []  # type: list[str]
        self.video_encoders = []  # type: list[str]
        self.subtitle_encoders = []  # type: list[str]

        self.muxing_formats = []  # type: list[str]
        self.demuxing_formats = []  # type: list[str]


class Inner:
    """
    Extract encoder information from codec description.
    """

    TIMEOUT = 3000

    def __init__(self):
        self.info = Info()

    def find_encoders_in_desc(self, target: list[str], s: str) -> int:
        keyword_begin = "(encoders:"
        keyword_end = ")"

        try:
            begin = s.index(keyword_begin)

        except ValueError:
            return 0  # encoder name not found in description

        begin += len(keyword_begin)

        try:
            end = s.index(keyword_end, begin)

        except ValueError:
            return 0  # error, mission ')'

        length = end - begin

        # encoder_str contains encoder names separated by spaces, and
        # may contain leading and trailing spaces.
        encoders_str = s[begin:begin + length]

        # split encoder_str into encoder names and skip whitespaces

        encoders = encoders_str.split(" ")
        encoders = [i.strip() for i in encoders if i.strip()]

        for e in encoders:
            target.append(e)  # fill codec names into the list

        return len(encoders)

    def read_ffmpeg_codecs(self, flag: str) -> bool:
        ffmpeg_process = QProcess()
        parameters = []  # type: list[str]

        parameters.append(flag)

        ffmpeg_process.setReadChannel(QProcess.ProcessChannel.StandardOutput)

        ffmpeg_process.start(ExePath.getPath('ffmpeg'), parameters)

        # Wait until ffmpeg has started.
        if not ffmpeg_process.waitForStarted(self.TIMEOUT):
            return false

        # Wait until ffmpeg has finished.
        if not ffmpeg_process.waitForFinished(self.TIMEOUT):
            return false

        if ffmpeg_process.exitCode() != 0:
            return false  # error

        # Find all available encoders
        pattern = "[ D]E([ VAS])...\\s+([^ ]+)\\s*(.*)$"
        encoder_list = []  # temporary storage of encoder names

        AV_INDEX = 1
        CODEC_NAME_INDEX = 2
        CODEC_DESC = 3

        self.info.ffmpeg_codec_info = ''

        while ffmpeg_process.canReadLine():
            line = ffmpeg_process.readLine()
            self.info.ffmpeg_codec_info += str(line)

