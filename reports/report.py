import os
import subprocess
import sys

from helper_methods import help
from reports.codeforces_report import codeforces_report
from reports.footer import footer
from reports.header import header


class report:

    @staticmethod
    def generate(complete_info):
        name = complete_info["name"]
        email = complete_info["email"]
        student_report = ""
        header_string = header.generate(name, email)
        codeforces_string = codeforces_report.generate(complete_info["codeforces"])
        footer_string = footer.generate()
        student_report = header_string + codeforces_string + footer_string
        print(student_report)
        report.make_file(student_report)
        report.compile_report()
        report.relocate_file(name)

    @staticmethod
    def make_file(student_report):
        path = os.path.join(sys.path[0], "latex_files", "OpenFonts", "deedy_resume-openfont.xtx")
        help.write_data_to_file(student_report, path)

    @staticmethod
    def compile_report():
        path_to_script = os.path.join(sys.path[0], "script.bat")
        subprocess.call([path_to_script])

    @staticmethod
    def relocate_file(name):
        source = os.path.join(sys.path[0], "latex_files", "OpenFonts", "deedy_resume-openfont.pdf")
        destination = os.path.join(sys.path[0], "student_pdf_files", name + ".pdf")
        path = os.path.join(sys.path[0], "latex_files", "OpenFonts")
        print(os.listdir(path))
        help.relocate_file(source, destination)
