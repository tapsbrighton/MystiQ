##
# Created by @taps on Wednesday, 02 April 2025.
##
import sys

from PySide6.QtCore import QProcess, QSettings

program_path = {}  # type: dict[str, str]


class ExePath:
    TIMEOUT = 3000

    @staticmethod
    def setPath(program: str, path: str) -> None:
        program_path[program] = path

    @staticmethod
    def getPath(program: str) -> str:
        try:
            return program_path[program]

        except KeyError as e:
            print(f'{e}', ExePath.getPath.__qualname__, file=sys.stderr)

            return ''

    @staticmethod
    def checkProgramAvailability(program: str) -> bool:
        """
        Check whether the program can be executed.
        :param program:
        :return:
        """
        try:
            path = ExePath.getPath(program)

            proc = QProcess()
            param = []

            # try to run the program
            proc.start(path, param)

            if not proc.waitForStarted(ExePath.TIMEOUT):
                # failed to start the program
                return False

            # successfully started the program, kill it immediately
            proc.kill()
            proc.waitForFinished(ExePath.TIMEOUT)

            return True

        except KeyError as e:
            #  the program is not set
            return False

    @staticmethod
    def saveSettings():
        """
        Save the paths using QSettings
        :return:
        """
        settings = QSettings()

        for name, path in program_path.items():
            settings.setValue(f'exepath/{name}', path)

    @staticmethod
    def loadSettings():
        """
        Load the paths using QSettings
        :return:
        """
        settings = QSettings()

        for name in program_path.keys():
            path = settings.value(f'exepath/{name}', program_path[name])

            path = str(path)

            program_path[name] = path

    @staticmethod
    def getPrograms() -> list[str]:
        return list(program_path.keys())
