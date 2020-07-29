import os
import sys

import requests
from bs4 import BeautifulSoup

from helper_methods import help


def question_type_extraction(link):
    link = help.strip_string(link)
    # print(link)
    return extract_number(link)


def extract_number(link):
    for i in range(len(link) - 1, -1, -1):
        if link[i] == '(':
            # print(link[i+1:len(link)-1])
            return link[i + 1:len(link) - 1]


class student_progress_info:
    def __init__(self):
        self.name: str = ""
        self.university: str = ""
        self.rank_in_institute = 0
        self.courses_attended = {}
        self.overall_coding_score = 0
        self.monthly_coding_score = 0
        self.subjective_score = 0
        self.weekly_coding_score = 0


class student_problem_solving_info:
    def __init__(self):
        self.total_problems_solved = 0
        self.school_level = 0
        self.basic_level = 0
        self.easy_level = 0
        self.medium_level = 0
        self.hard_level = 0


class student_article_info:
    pass


class geeks_for_geeks:
    def __init__(self, handle):
        self.website_link = "https://auth.geeksforgeeks.org"
        self.student_link = self.website_link + "/user/" + handle
        self.university_link = ""
        self.student_info = student_progress_info()
        self.problems_info = student_problem_solving_info()
        self.article_info = student_article_info()
        self.extract_progress_data()
        self.extract_problem_solving_data()
        self.extract_articles_data()

    def send_request(self, tab):
        try:
            response = requests.get(self.student_link + tab)
            if response.status_code == 200:
                return response
        except Exception as ex:
            print(ex)

    def write_data_to_file(self, response, file_name):
        try:
            file_path = os.path.join(sys.path[0], file_name)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
        except Exception as ex:
            print(ex)

    def extract_progress_data(self):
        response = self.send_request("/practice/")
        file_name = "geeks_for_geeks_student_progress.html"
        file_path = os.path.join(sys.path[0], file_name)
        self.write_data_to_file(response, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            action_container = soup.find("div", attrs={
                "class": "mdl-cell mdl-cell--7-col mdl-cell--12-col-phone whiteBgColor mdl-shadow--2dp userMainDiv"})
            information_divs = action_container.find_all("div", attrs={"class": "mdl-grid"})
            name = information_divs[0].find_all("div")[1].string
            name = help.strip_string(name)
            self.student_info.name = name
            university_info = information_divs[1].find_all("div")[1].find("a")
            university_name = university_info.string
            self.student_info.university = university_name
            university_name = help.strip_string(university_name)
            university_link = university_info['href']
            university_link = help.strip_string(university_link)
            self.university_link = university_link
            # print(self.student_info.name,self.student_info.university,self.university_link)
            rank = information_divs[2].find_all("div")[1].string
            rank = help.strip_string(rank, "#")
            self.student_info.rank_in_institute = rank
            # print(self.student_info.rank_in_institute)
            all_courses = information_divs[3].find_all("div")[1].find_all("a")
            for course in all_courses:
                name = course.string
                name = help.strip_string(name)
                link = course['href']
                link = help.strip_string(link)
                self.student_info.courses_attended[name] = link
            # for name,link in self.student_info.courses_attended.items():
            #     print(name,link)
            coding_score = information_divs[4].find_all("div")[0].string
            self.student_info.overall_coding_score = coding_score
            score_div = information_divs[5].find_all("div")
            monthly_score = score_div[0].find("span").string
            monthly_score = help.strip_string(monthly_score)
            weekly_score = score_div[1].find("span").string
            weekly_score = help.strip_string(weekly_score)
            self.student_info.monthly_coding_score = monthly_score
            self.student_info.weekly_coding_score = weekly_score
            subjective_score = information_divs[6].find_all("div")[0].find("span").string
            subjective_score = help.strip_string(subjective_score)
            self.student_info.subjective_score = subjective_score
            # print(self.student_info.subjective_score)

    def extract_problem_solving_data(self):
        try:
            file_name = "geeks_for_geeks_student_progress.html"
            file_path = os.path.join(sys.path[0], file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                problems_div = soup.find("div", attrs={"id": "problem-solved-div"})
                problems = problems_div.find_all("a")
                self.problems_info.school_level = question_type_extraction(problems[0].string)
                self.problems_info.basic_level = question_type_extraction(problems[1].string)
                self.problems_info.easy_level = question_type_extraction(problems[2].string)
                self.problems_info.medium_level = question_type_extraction(problems[3].string)
                self.problems_info.hard_level = question_type_extraction(problems[4].string)
                # print(self.problems_info.school_level,self.problems_info.basic_level)
                # print(self.problems_info.medium_level,self.problems_info.hard_level)
            help.remove_file(file_path)
        except Exception as ex:
            print(ex)

    def extract_articles_data(self):
        pass
