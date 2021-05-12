class DictsMerger:
    """
        Assigns students to corresponding rooms
    """

    def __init__(self, rooms, students):
        self.rooms = rooms
        self.students = students

    def merge(self):
        merged_data = self.rooms
        self._assign_students(merged_data)
        return merged_data

    def _assign_students(self, rooms_list):
        """
            Loop at students list and assign them to corresponding rooms.
        """
        for student_dict in self.students:
            student = student_dict.copy()
            student.pop('room')
            rooms_list[student_dict.get('room')].setdefault('students', []).append(student)
        return rooms_list
