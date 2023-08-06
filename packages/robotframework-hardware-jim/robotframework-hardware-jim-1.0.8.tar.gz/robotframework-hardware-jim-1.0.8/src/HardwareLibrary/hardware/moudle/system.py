import sys
import os
import subprocess
from typing import Union



class SystemBase():

    def __init__(self) -> None:
        pass
    
    def run_powershell(self, cmd: Union[str, list]):

        args = ["powershell", "-ExecutionPolicy", "Unrestricted"]
        command = args + cmd if isinstance(cmd, list) else args + [cmd]
        
        try:
            output = subprocess.check_output(command, shell=True).decode()
        except subprocess.CalledProcessError as e:
            raise Exception(f"CalledProcessError: {e.output}")
        
        return output