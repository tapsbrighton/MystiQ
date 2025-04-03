##
# Created by @taps on Wednesday, 02 April 2025.
##

from PySide6.QtCore import QObject, QProcess

"""
SoX provides much more audio-processing options than
  ffmpeg, yet it doesn't accept as many formats as
  ffmpeg does. In this pipeline, format conversion
  is done by ffmpeg and audio processing is done by SoX.

  The audio-filtering pipeline consists of two stages:

  1. Audio Extraction
     command: ffmpeg -i <infile> -vn -f <fmt> -
     input: infile
     output: stdout
     Extract the audio stream from the input file, convert it
     into sox format, and pipe it to stdout.

  2. Audio Filtering
     command: sox -t <fmt> - -t <fmt> - <options>
     input: stdin
     output: stdout
     Process the audio stream using SoX. The output is piped to
     stdout.
     """


class AudioFilter(QObject):
    TIMEOUT = 3000

    def __init__(self, parent=None):
        super(AudioFilter, self).__init__(parent)

        self.z = 'AudioFilter:'

        self.extractAudioProc = QProcess(self)
        self.soxProc = QProcess(self)

        muxing = FFmpegInterface.getSupportedMuxingFormats()  # type: set[str]
        demuxing = FFmpegInterface.getSupportedDemuxingFormats()  # type: set[str]

        ans1 = 'sox' in muxing
        ans2 = 'sox' in demuxing
        self.useSoxFormat = ans1 and ans2



    def start(self, params: ConversionParameters, dest: QProcess):
        """
        Start the audio-filtering process pipeline.
        :param param: the conversion parameter
        :param dest: the process to receive the output from stdin
        :return:
        """
        ffmpeg_param = []  # type: list[str]
        sox_param = []  # type: list[str]

        if self.useSoxFormat:
            fmt = 'sox'
        else:
            fmt = 'flac'

        if self.soxProc.state() != QProcess.ProcessState.NotRunning:
            # still running
            self.soxProc.kill()
            self.soxProc.waitForFinished(self.TIMEOUT)

        if self.extractAudioProc.state() != QProcess.ProcessState.NotRunning:
            # still running
            self.extractAudioProc.kill()
            self.extractAudioProc.waitForFinished(self.TIMEOUT)

        # ffmpeg process settings
        ffmpeg_param.append('-i')
        ffmpeg_param.append(params.source)
        ffmpeg_param.append("-vn")
        ffmpeg_param.append('-f')
        ffmpeg_param.append(fmt)
        ffmpeg_param.append('-')

        self.extractAudioProc.setStandardOutputProcess(self.soxProc)

        # sox process settings
        sox_param.append('-t')
        sox_param.append(fmt)
        sox_param.append('-')
        sox_param.append('-t')
        sox_param.append(fmt)
        sox_param.append('-')

        if params.speed_scaling:
            sox_param.append('tempo')
            sox_param.append(str(params.speed_scaling_factor))

        self.soxProc.setStandardOutputProcess(dest)

        print(f'{self.z} Ffmpeg params: "{ffmpeg_param}"')
        print(f'{self.z} SoX params: "{sox_param}"')

        # start the two processes
        self.extractAudioProc.start(ExePath.getPath('ffmpeg'), ffmpeg_param)
        self.soxProc.start(ExePath.getPath('sox'), sox_param)

        return self.extractAudioProc.waitForStarted(self.TIMEOUT) and self.extractAudioProc.waitForStarted(self.TIMEOUT)

    @staticmethod
    def available():
        """
        Check if execution conditions are met.
        :return: true if AudioFilter works, false otherwise.
        """
        sox_process = QProcess()

        sox_process.start(ExePath.getPath('sox'), [])

        return sox_process.waitForStarted(AudioFilter.TIMEOUT)
