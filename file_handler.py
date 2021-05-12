from abc import ABC, abstractmethod
from dict2xml import dict2xml
from json import dumps, loads
from os import getcwd, mkdir
from os.path import exists
from sys import exit
from my_exception import MyException


class AbstractExporter(ABC):

    @abstractmethod
    def export(self, data):
        pass


class JSONExporter(AbstractExporter):
    """
        Exports data to json format
    """
    extension = '.json'

    def export(self, data):
        return dumps(data)


class XMLExporter(AbstractExporter):
    """
        Exports data to xml format
    """

    extension = '.xml'

    def export(self, data):
        return dict2xml(data)


class FileHandler:
    """
        Handles file processing
    """

    def __init__(self, exporter):
        self.exporter = exporter

    def read(self, file_path):
        with open(file_path, 'r') as f:
            data = f.read()
            data = self._deserialize_json(data)
            return data

    def write(self, merged_data):
        export_data = self.exporter().export(merged_data)
        folder_path = getcwd() + '/output_data/'
        file_path = folder_path + 'output' + self.exporter.extension
        if not exists(folder_path):
            mkdir(folder_path)
        with open(file_path, 'w') as f:
            f.write(export_data)

    @staticmethod
    def _deserialize_json(data):
        return loads(data)


class ArgsHandler:
    """
        Validates input arguments
    """

    _args_quantity = 4
    _formats = ('xml', 'json')

    def __init__(self, args):
        self.args = args

    def get_exporter(self):
        if self.args[3] == 'xml':
            return XMLExporter
        return JSONExporter

    def validate_args(self):
        try:
            if len(self.args) != self._args_quantity:
                raise MyException('Incorrect number of input arguments, should be 3.')
            elif not exists(self.args[1]):
                raise MyException('Incorrect path to first file.')
            elif not exists(self.args[2]):
                raise MyException('Incorrect path to second file.')
            elif self.args[3] not in self._formats:
                raise MyException('Incorrect format of export.')

        except MyException as err:
            print(err.args[0])
            exit()
        except (IndexError, FileNotFoundError):
            exit()
