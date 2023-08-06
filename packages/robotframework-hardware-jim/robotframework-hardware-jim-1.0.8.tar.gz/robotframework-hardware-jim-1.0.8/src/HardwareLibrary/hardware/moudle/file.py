import sys
import os
import ftplib
import yaml
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class FTPUtils:
    def __init__(self, server: str, username: str, password: str):
        self.ip = server
        self.ftp = ftplib.FTP(server)
        self.ftp.login(username, password)
        self.download_buffer = 1024
        self.upload_buffer = 1024

    def change_dir(self, work_dir):
        return self.ftp.cwd(work_dir)

    def get_working_dir(self):
        return self.ftp.pwd()

    def get_item_list(self, work_dir):
        self.ftp.cwd(work_dir)
        return self.ftp.nlst()

    def is_item_file(self, item):
        try:
            self.ftp.cwd(item)
            self.ftp.cwd('..')
            return False
        except ftplib.error_perm as fe:
            if not fe.args[0].startswith('550'):
                raise
            return True

    def download_file(self, file_name, save_as_name):
        file_handler = open(save_as_name, 'wb')
        self.ftp.retrbinary("RETR " + file_name, file_handler.write, self.download_buffer)
        file_handler.close()
        return save_as_name

    def download_dir(self, dir_name, save_as_dir):
        if not os.path.exists(save_as_dir):
            os.mkdir(save_as_dir)
        self.ftp.cwd(dir_name)
        for item in self.ftp.nlst():
            if self.is_item_file(item):
                self.download_file(item, os.path.join(save_as_dir, item))
            else:
                self.download_dir(item, os.path.join(save_as_dir, item))
        self.ftp.cwd("..")
        return save_as_dir

    def upload_file(self, file_name, save_as_name):
        try:
            self.ftp.storbinary('STOR ' + save_as_name, open(file_name, 'rb'), self.upload_buffer)
            return save_as_name
        except Exception as e:
            print('Exception occurred when uploading file to FTP server path {}. Exception as below: \n\
            {}'.format(save_as_name, e))

    def new_dir(self, dir_name):
        try:
            self.ftp.mkd(dir_name)
        # ignore "directory already exists"
        except ftplib.error_perm as fe:
            if not fe.args[0].startswith('550 Cannot create a file when that file already exists'):
                raise
            # return False
        return dir_name

    def upload_dir(self, dir_path, save_as_dir):
        try:
            self.ftp.cwd(save_as_dir)
        except ftplib.error_perm as fe:
            if fe.args[0].startswith('550'):
                self.new_dir(save_as_dir)
                self.ftp.cwd(save_as_dir)
        for item_name in os.listdir(dir_path):
            local_path = os.path.join(dir_path, item_name)
            if os.path.isfile(local_path):
                self.ftp.storbinary('STOR ' + item_name, open(local_path, 'rb'), self.upload_buffer)
            elif os.path.isdir(local_path):
                ftp_folder = self.new_dir(item_name)
                self.upload_dir(local_path, ftp_folder)
                self.ftp.cwd("..")
        return save_as_dir

    def delete_file(self, file_name):
        self.ftp.delete(file_name)
        return file_name

    def delete_dir(self, dir_name):
        # Handle dir_name doesn't exist
        try:
            self.change_dir(dir_name)
            items = self.ftp.nlst()
        except ftplib.all_errors as e:
            return
        for item in items:
            if os.path.split(item)[1] in ('.', '..'):
                continue
            try:
                self.change_dir(item)
                # self.change_dir('../../../../..')
                self.change_dir('../..')
                self.delete_dir(item)
            except ftplib.all_errors:
                self.delete_file(item)
        try:
            # self.change_dir('../../../../..')
            self.change_dir('../..')
            self.ftp.rmd(dir_name)
        except ftplib.all_errors as e:
            print(e)
        return dir_name

    def close(self):
        self.ftp.close()

class XMLOperator:
    def __init__(self, file_path):
        self.tree = ET.parse(file_path)

    def get_root(self):
        return self.tree.getroot()

    def find_nodes(self, path):
        return self.tree.findall(path)

    @staticmethod
    def attrib(node):
        return node.attrib

    @staticmethod
    def tag(node):
        return node.tag

    def write(self, file_path):
        self.tree.write(file_path)

    @staticmethod
    def get_value(node, name):
        return node.attrib[name]

    @staticmethod
    def set_value(node, name, value):
        node.set(name, value)

    @staticmethod
    def iter(node):
        return node.iter()


class YamlOperator:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r') as f:
            result = yaml.safe_load(f)
        return result

    def write(self, content):
        if not os.path.exists(self.file_path):
            open(self.file_path, 'w').close()
        with open(self.file_path, 'w')as f1:
            yaml.safe_dump(content, f1)


class TxtOperator:
    def __init__(self, filename, mode='a', encoding='utf8'):
        self._filename = filename
        self._mode = mode
        self._encoding = encoding

    def _get_read(self):
        return open(self._filename, 'r', encoding=self._encoding)

    def _get_write(self):
        return open(self._filename, 'w' if self._mode == 'w' else 'a', encoding=self._encoding)

    def get_lines(self):
        f = self._get_read()
        lines = f.readlines()
        f.close()
        return lines

    def get_source(self):
        f = self._get_read()
        source = f.read()
        f.close()
        return source

    def set_msg(self, msg):
        f = self._get_write()
        f.write(msg)
        f.close()

    def replace_msg(self, new, old):
        data = self.get_source()
        new_data = data.replace(old, new)
        self.set_msg(new_data)