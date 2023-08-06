import sys
import os
from robotlibcore import keyword
from HardwareLibrary.hardware.moudle.system import SystemBase



class SystemKeywords:
    """
    Interface implementation from robotframework usage for file keywords.
    """
    
    def __init__(self):
        pass
    
    @keyword
    def set_regional_format(self, language):
        """set_regional_format

        Arguments:
        | Argument      | Type            | Description                 |
        | language      | str             |                             |

        language = ["zh-CN", "en-US"]
        
        Examples:
        | Set Regional Format  <language>  |
        
        """
        SystemBase().run_powershell(["Set-Culture", language])
        
    
    @keyword
    def get_regional_format(self):
        """get_regional_format

        Examples:
        | Get Regional Format  |
        
        """
        
        return SystemBase().run_powershell(["Get-Culture"])
        