import sys
import os
from robotlibcore import keyword
from HardwareLibrary.hardware.moudle.file import FTPUtils
from HardwareLibrary.hardware.moudle.system import SystemBase


LOCAL_DOWNLOAD_PATH = os.path.join(os.path.expanduser('~'), "Downloads")
   
   
class FileKeywords:
    """
    Interface implementation from robotframework usage for file keywords.
    """
    
    def __init__(self):
        pass
    
    @keyword
    def download_thinupdate_package(self, ftp_account, package, version, local_path=LOCAL_DOWNLOAD_PATH):
        """Copy specific version setup_package from ftp server.

        Arguments:
        | Argument      | Type            | Description                 |
        | ftp_account   | dict            |                             |
        | package       | string          | setup_package name          |
        | version       | string          | setup_version               |
        | local_path    | string          | download into a local_path  |
        
        ftp_account = {
            "host": "ip address",
            "user": "username",
            "passwd": "password",
            "workspace": "project folder path"
        }

        Examples:
        | Download Thinupdate Package  <ftp_account>  <package>  <version>  <local_path> |
        
        """

        
        ftp_utils = FTPUtils(ftp_account['host'], ftp_account['user'], ftp_account['passwd'])
        ftp = ftp_utils.ftp
        # cwd folder: workspace/version 
        ftp.cwd(f"{ftp_account['workspace']}/{version}")
        
        # find SETUP_PACKAGE folder
        while True:
            if package in ftp.nlst():
                print(f"{package} in current folder: {ftp.pwd()}")
                break
            else:
                for item in ftp.nlst():
                    if "P012S7." in item or version in item:
                        path = item
                    else:
                        if "." not in item and not item.startswith("sp"):
                            path = item
                ftp.cwd(path)
        
        local_package = os.path.join(local_path, package)
        ftp_utils.download_file(package, local_package)
        ftp_utils.close()
    
    @keyword
    def install_thinupdate_package(self, package, local_path=LOCAL_DOWNLOAD_PATH):
        """Install ThinUpdate package.

        Arguments:
        | Argument          | Type      | Description                          |
        | package           | string    | setup_package name                   |
        | local_path        | string    | download into a local_path           |

        Examples:
        | Install Thinupdate Package  <package>  <local_path>                  |
        """
        
        # install ThinUpdate package
        local_package = os.path.join(local_path, package)
        SystemBase().run_powershell(["msiexec", f"/i {local_package}", "/qb"])