from abc import ABC, abstractmethod
from argparse import ArgumentParser
from json import dumps, loads
from os import getcwd, mkdir
from os.path import exists
from sys import exit

from dict2xml import dict2xml

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

    def __init__(self):
        self.args = ArgsHandler()
        self.students = self.read(self.args.get_students_path())
        self.rooms = self.read(self.args.get_rooms_path())
        self.exporter = self.args.get_exporter()

    def merge(self):
        merged_data = self.rooms
        self._assign_students(merged_data)
        return merged_data

    def read(self, file_path):
        with open(file_path, 'r') as f:
            data = f.read()
            data = self._deserialize_json(data)
            return data

    def write(self):
        merged_data = self.merge()
        export_data = self.exporter().export(merged_data)
        folder_path = getcwd() + '/output_data/'
        file_path = folder_path + 'output' + self.exporter.extension
        if not exists(folder_path):
            mkdir(folder_path)
        with open(file_path, 'w') as f:
            f.write(export_data)

    def _assign_students(self, rooms_list):
        """
            Loop at students list and assign them to corresponding rooms.
        """
        for student_dict in self.students:
            student = student_dict.copy()
            student.pop('room')
            rooms_list[student_dict.get('room')].setdefault('students', []).append(student)
        return rooms_list

    @staticmethod
    def _deserialize_json(data):
        return loads(data)


class ArgsHandler:
    """
        Validates input arguments
    """

    _formats = ('xml', 'json')

    def __init__(self):
        self.args = self.parse_args()
        self.validate_args()

    def get_exporter(self):
        if self.args.format == 'xml':
            return XMLExporter
        return JSONExporter

    def get_rooms_path(self):
        return self.args.rooms_path

    def get_students_path(self):
        return self.args.students_path

    @staticmethod
    def parse_args():
        parser = ArgumentParser()
        parser.add_argument('students_path', help='Path to file with students.')
        parser.add_argument('rooms_path', help='Path to file with rooms.')
        parser.add_argument('format', help='Format of export.')
        return parser.parse_args()

    def validate_args(self):
        try:
            if not exists(self.args.students_path):
                raise MyException('Incorrect path to first file.')
            elif not exists(self.args.rooms_path):
                raise MyException('Incorrect path to second file.')
            elif self.args.format not in self._formats:
                raise MyException('Incorrect format of export.')

        except MyException as err:
            print(err.args[0])
            exit()
        except (IndexError, FileNotFoundError):
            exit()
