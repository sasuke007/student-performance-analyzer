import os
import sys

import requests
from bs4 import BeautifulSoup

import helper_methods.help as help


def display_questions(questions_list):
    for question_name, question_link in questions_list.items():
        print(question_name, question_link)


def remove_file(file_name):
    file_path = os.path.join(sys.path[0], file_name)
    if os.path.exists(file_path):
        os.remove(file_path)


class complete_info:
    def __init__(self):
        self.reputation = 0
        self.questions = {}
        self.answers = {}


class stack_overflow:
    def __init__(self, handle):
        self.handle = handle
        self.website_link = "https://stackoverflow.com"
        self.student_link = self.website_link + "/users/" + handle + "/"
        self.student_info = complete_info()
        self.extract_questions()
        self.extract_answers()

    def send_request(self, tab):
        try:
            response = requests.get(self.student_link + tab)
            if response.status_code == 200:
                return response
            raise Exception("Error in making request")
        except Exception as e:
            print(e)

    def write_data_to_file(self, response, name):
        try:
            with open(os.path.join(sys.path[0], "stack_overflow_" + name + ".html"), "w", encoding="utf-8") as file:
                file.write(response.text)
        except Exception as e:
            print(e)

    def extract_questions(self):
        try:
            response = self.send_request("?tab=questions")
            self.write_data_to_file(response, "questions")
            with open(os.path.join(sys.path[0], "stack_overflow_questions.html"), "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                reputation = soup.find("div", attrs={"class": "grid gs8 fs-headline1"}).find("span").string
                reputation = help.strip_string(reputation)
                self.student_info.reputation = reputation
                # print(self.student_info.reputation)
                questions_list = soup.find("div", attrs={"class": "user-questions"}).find_all("div", attrs={
                    "class": "question-summary narrow"})
                for question in questions_list:
                    name = question.find("a").string
                    name = help.strip_string(name)
                    link = question.find("a")['href']
                    link = self.website_link + help.strip_string(link)
                    self.student_info.questions[name] = link
                # display_questions(self.student_info.questions)
            remove_file("stack_overflow_questions.html")
        except Exception as e:
            print(e)

    def extract_answers(self):
        try:
            response = self.send_request("?tab=answers")
            self.write_data_to_file(response, "answers")
            with open(os.path.join(sys.path[0], "stack_overflow_answers.html"), "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                answers_list = soup.find_all("div", attrs={"class": "answer-summary"})
                for answer in answers_list:
                    name = answer.find("a").string
                    name = help.strip_string(name)
                    link = answer.find("a")['href']
                    link = self.website_link + help.strip_string(link)
                    self.student_info.answers[name] = link
                # display_questions(self.student_info.answers)
            remove_file("stack_overflow_answers.html")
        except Exception as ex:
            print(ex)
