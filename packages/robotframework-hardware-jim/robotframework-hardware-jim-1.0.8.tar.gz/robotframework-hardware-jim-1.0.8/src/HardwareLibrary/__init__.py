# pylint: disable=invalid-name
from enum import Enum
from robot.libraries.BuiltIn import BuiltIn
from robotlibcore import DynamicCore
from HardwareLibrary import version
from HardwareLibrary.keywords import (FileKeywords, SystemKeywords)

# pylint: enable=invalid-name
class HardwareLibrary(DynamicCore):
    """
    HardwareLibrary is a Robot Framework library for automating Windows GUI.
    And it will be used in all HP robotframework projects
    """
    ROBOT_LIBRARY_VERSION = version.VERSION
    ROBOT_LIBRARY_SCOPE = "Global"
    ROBOT_LISTENER_API_VERSION = 2

    class RobotMode(Enum):
        """
        Actual state from test execution by robot framework.
        """
        TEST_NOT_RUNNING = 1
        TEST_RUNNING = 2

    class KeywordModules(Enum):
        """
        Enumeration from all supported keyword modules.
        """
        FILE = "File"
        SYSTEM = "System"
        

    def __init__(self):
        """
        HardwareLibrary can be imported by following optional arguments:

        """

        self.mode = HardwareLibrary.RobotMode.TEST_NOT_RUNNING
        self.builtin = BuiltIn()

        self.keyword_modules = {
            HardwareLibrary.KeywordModules.FILE: FileKeywords(),
            HardwareLibrary.KeywordModules.SYSTEM: SystemKeywords(),
        }

        # Robot init
        self.ROBOT_LIBRARY_LISTENER = self  # pylint: disable=invalid-name
        self.libraries = self.keyword_modules.values()
        DynamicCore.__init__(self, self.libraries)