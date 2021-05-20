def merge(rooms, students):
    """
        Loop at students list and assign them to corresponding rooms.
    """

    merged_data = rooms
    for student_dict in students:
        student = student_dict.copy()
        student.pop('room')
        merged_data[student_dict.get('room')].setdefault('students', []).append(student)
    return merged_data
