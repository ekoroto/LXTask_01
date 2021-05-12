import file_handler
from merge_files import DictsMerger
from sys import argv


if __name__ == '__main__':

    args = file_handler.ArgsHandler(argv)
    args.validate_args()

    handler = file_handler.FileHandler(args.get_exporter())
    students = handler.read(argv[1])
    rooms = handler.read(argv[2])

    merged_data = DictsMerger(rooms, students).merge()
    handler.write(merged_data)
