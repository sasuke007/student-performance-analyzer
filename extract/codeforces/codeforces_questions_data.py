import os
import sys

from bs4 import BeautifulSoup

import helper_methods.help as help


class codeforces_questions_data:
    handle = None
    questions_list = {}
    website_link = "https://codeforces.com"
    questions_page_link = None
    total_pages = 0
    soup_object = None
    html_page = None

    def __init__(self, handle):
        self.handle = handle
        self.questions_page_link = self.website_link + "/submissions/" + self.handle
        self.extract_data()

    def get_questions_list(self):
        return self.questions_list

    def get_question_page_url(self, page_no):
        return self.website_link + "/submissions/" + self.handle + "/page/" + str(page_no)

    def extract_data(self):
        self.html_page = help.send_request(self.questions_page_link).text
        help.write_data_to_file(self.html_page, os.path.join(sys.path[0], "something"))
        self.set_soup_object()
        self.get_total_pages()
        for page_no in range(1, self.total_pages + 1):
            page_url = self.get_question_page_url(page_no)
            self.html_page = help.send_request(page_url).text
            self.set_soup_object()
            help.write_data_to_file(self.html_page, os.path.join(sys.path[0], "something"))
            self.get_questions_data()

    def get_question(self, table_data):
        verdict = table_data[5].get_text().strip()
        if verdict == "Accepted":
            question_name = table_data[3].get_text().strip()
            question_link = table_data[3].a['href']
            question_link = self.website_link + question_link
            print(question_name, question_link)
            self.questions_list[question_name] = question_link

    def get_questions_data(self):
        questions_table_class = {"class": "status-frame-datatable"}
        questions_table = self.soup_object.find("table", attrs=questions_table_class)
        table_rows = questions_table.find_all("tr")
        for row_no in range(len(table_rows)):
            # zero th row does not contain any information
            if row_no == 0:
                continue
            table_data = table_rows[row_no].find_all("td")
            self.get_question(table_data)
            # for data in table_data:
            #     print(data.get_text().strip(), end=" ")
            # print()

    def get_total_pages(self):
        pagination_div_class = {"class", "pagination"}
        pagination_tag = self.soup_object.find_all("div", attrs=pagination_div_class)
        # 1 subscript is used because the second div which has class pagination has the required information
        ul = pagination_tag[1].ul
        li = ul.find_all("li")
        all_li = len(li)
        # -2 is done because that is the last page
        last_li_tag = li[all_li - 2]
        total_pages = last_li_tag.get_text().strip()
        self.total_pages = int(total_pages)

    def set_soup_object(self):
        self.soup_object = BeautifulSoup(self.html_page, "html.parser")


def main():
    cqd = codeforces_questions_data("tourist")


if __name__ == "__main__":
    main()
