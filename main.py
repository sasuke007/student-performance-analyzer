import os
import sys

from data_objects import student_data


def main():
    with open(os.path.join(sys.path[0], "students_handle/rohit.handle"), "r") as file:
        student_handles = {}
        for line in file:
            handle = line.split(":")
            student_handles[handle[0]] = handle[1].strip('\n')

    s = student_data.student("rohit", "pandit.rohit0007@gmail.com", student_handles)
    s.generate_report()


if __name__ == '__main__':
    main()
