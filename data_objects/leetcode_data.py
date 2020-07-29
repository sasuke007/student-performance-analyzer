import os
import sys

import requests
from bs4 import BeautifulSoup

import helper_methods.help as help


class contests_data:
    def __init__(self):
        self.finished_contests = 0
        self.rating = 0
        self.global_rank = 0
        self.total_candidates = 0


class progress_data:
    def __init__(self):
        self.solved_questions = 0
        self.total_questions = 0
        self.accepted_submissions = 0
        self.total_submissions = 0


class contributions_data:
    def __init__(self):
        self.coins = 0
        self.problems_contributed = 0
        self.test_cases_contributed = 0


class questions_data:
    def __init__(self):
        self.questions_list = {}


def delete_html_file():
    if os.path.exists(os.path.join(sys.path[0], "leetcode.html")):
        os.remove(os.path.join(sys.path[0], "leetcode.html"))


class leetcode:
    # This class will contain all the data retrieved from leetcode and methods required
    # to manipulate and extract that data
    def __init__(self, handle):
        self.handle: str = handle
        self.student_link: str = "https://leetcode.com/" + handle + "/"
        self.website_link: str = "https://leetcode.com"
        self.contests = contests_data()
        self.progress = progress_data()
        self.contributions = contributions_data()
        self.questions = questions_data()
        self.extract_data()
        delete_html_file()
        self.display()

    def display(self):
        print("finished_contests : ", self.contests.finished_contests)
        print("rating : ", self.contests.rating)
        print("global_rank : ", str(self.contests.global_rank) + "/" + str(self.contests.total_candidates))
        print("solved_questions : ", self.progress.solved_questions)
        print("total_questions : ", self.progress.total_questions)
        print("accepted_submissions : ", self.progress.accepted_submissions)
        print("total_submissions : ", self.progress.total_submissions)
        print("questions info")
        for name, link in self.questions.questions_list.items():
            print(name, link)

    def extract_contests_information(self, contest_information):
        try:
            list_items = contest_information.find_all('li')
            contests_played = list_items[0].find('span').string
            contests_played = help.strip_string(contests_played)
            self.contests.finished_contests = int(contests_played)
            rating = list_items[1].find('span').string
            rating = help.strip_string(rating)
            self.contests.rating = int(rating)
            ranking = list_items[2].find('span').string
            ranking = help.split_string(ranking)
            self.contests.global_rank = int(ranking[0])
            self.contests.total_candidates = int(ranking[1])
            # print(self.contests.finished_contests)
            # print(self.contests.rating)
            # print(self.contests.global_rank)
            # print(self.contests.total_candidates)
        except Exception as ex:
            print(ex)

    def extract_progress_information(self, progress_information):
        try:
            list_items = progress_information.find_all('li')
            solved = list_items[0].find('span').string
            solved = help.split_string(solved)
            self.progress.solved_questions = int(solved[0])
            self.progress.total_questions = int(solved[1])
            submissions = list_items[1].find('span').string
            submissions = help.split_string(submissions)
            self.progress.accepted_submissions = int(submissions[0])
            self.progress.total_submissions = int(submissions[1])
            # print(self.progress.solved_questions)
            # print(self.progress.total_questions)
            # print(self.progress.accepted_submissions)
            # print(self.progress.total_submissions)
        except Exception as ex:
            print(ex)

    def extract_contributions_information(self, contributions_information):
        list_items = contributions_information.find_all('li')
        points = list_items[0].find('span').string
        points = help.strip_string(points)
        self.contributions.coins = int(points)
        problems = list_items[1].find('span').string
        problems = help.strip_string(problems)
        self.contributions.problems_contributed = int(problems)
        test_cases = list_items[2].find('span').string
        test_cases = help.strip_string(test_cases)
        self.contributions.test_cases_contributed = int(test_cases)
        # print(self.contributions.coins)
        # print(self.contributions.problems_contributed)
        # print(self.contributions.test_cases_contributed)

    def extract_profile_information(self, profile_information):
        profile_information = profile_information[0]
        information_divs = profile_information.find_all("div", attrs={"class": "panel panel-default"})
        self.extract_contests_information(information_divs[1])
        self.extract_progress_information(information_divs[2])
        self.extract_contributions_information(information_divs[3])

    def extract_questions_information(self, questions_information):
        try:
            questions_information = questions_information[0]
            # print(questions_information)
            questions_div = questions_information.find_all("div", attrs={"class": "panel panel-default"})[4]
            questions_list = questions_div.find_all('a')
            for question in questions_list:
                status = question.find_all('span')[0].string
                status = help.strip_string(status)
                if status == "Accepted":
                    name = str(question.find_all('b')[0].string)
                    link = self.website_link + str(question['href'])
                    self.questions.questions_list[name] = link
            # self.display_questions_list()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)

    def display_questions_list(self):
        for question_name, question_link in self.questions.questions_list.items():
            print(question_name, question_link)

    def extract_data(self):
        with open(os.path.join(sys.path[0], "leetcode.html"), "w+", encoding="utf-8") as file:
            try:
                html = requests.get(self.student_link)
                file.write(html.text)
                file.seek(0, 0)
                soup = BeautifulSoup(file, "html.parser")
                left_section_class = {"class": "col-sm-5 col-md-4"}
                right_section_class = {"class": "col-sm-7 col-md-8"}
                # profile_information contains reference to left section of leetcode page reference
                # where information like contest,rating,rankings are available
                profile_information = soup.find_all("div", attrs=left_section_class)
                self.extract_profile_information(profile_information)
                # questions_information contains reference to right section of leetcode page where
                # questions list and rating chart are available
                questions_information = soup.find_all("div", attrs=right_section_class)
                self.extract_questions_information(questions_information)
            except Exception as ex:
                return ex


def main():
    l = leetcode("user4391")


if __name__ == "__main__":
    main()
