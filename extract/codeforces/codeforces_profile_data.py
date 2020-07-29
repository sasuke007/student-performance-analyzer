import os
import sys

from bs4 import BeautifulSoup

import helper_methods.help as help


class codeforces_profile_data:
    handle = None
    website_link = None
    student_profile_link = None
    rank = None
    current_rating = None
    max_rating = None
    contribution = None
    friends = None
    registered_on = None
    html_page = None
    soup_object = None

    def __init__(self, handle):
        self.handle = handle
        self.website_link = "https://codeforces.com/"
        self.student_profile_link = self.website_link + "profile/" + self.handle
        self.extract_data()
        self.soup_object = None
        self.html_page = None

    def extract_data(self):
        self.html_page = help.send_request(self.student_profile_link).text
        help.write_data_to_file(self.html_page, os.path.join(sys.path[0], "something"))
        self.set_soup_object()
        self.set_rank()
        self.set_current_rating()
        self.set_max_rating()
        self.set_contribution()
        self.set_friends()
        self.set_registered_on()

    def get_rank(self):
        return self.rank

    def get_current_rating(self):
        return self.current_rating

    def get_max_rating(self):
        return self.max_rating

    def get_contribution(self):
        return self.contribution

    def get_friends(self):
        return self.friends

    def get_registered_on(self):
        return self.registered_on

    def set_rank(self):
        rank_tag_class = {"class": "user-rank"}
        self.rank = self.soup_object.find("div", attrs=rank_tag_class).find("span").get_text()
        # print(self.rank)

    def get_li_tags(self):
        profile_info_class = {"class": "info"}
        info_tag = self.soup_object.find("div", attrs=profile_info_class)
        ul_tag = info_tag.find("ul")
        li_tags = ul_tag.find_all("li")
        return li_tags

    def get_student_profile_link(self):
        return self.student_profile_link

    def set_current_rating(self):
        li_tags = self.get_li_tags()
        self.current_rating = li_tags[0].span.get_text()

    def set_max_rating(self):
        li_tags = self.get_li_tags()
        max_rating_tag = {"class": "smaller"}
        self.max_rating = li_tags[0].find("span", attrs=max_rating_tag).find_all("span")[1].get_text()
        # print(self.max_rating)

    def set_friends(self):
        li_tags = self.get_li_tags()
        self.friends = li_tags[2].get_text().strip()
        # print(self.friends)

    def set_contribution(self):
        li_tags = self.get_li_tags()
        self.contribution = li_tags[1].span.get_text()
        # print(self.contribution)

    def set_registered_on(self):
        li_tags = self.get_li_tags()
        self.registered_on = li_tags[4].span.get_text()
        # print(self.registered_on)

    def set_soup_object(self):
        self.soup_object = BeautifulSoup(self.html_page, "html.parser")


def main():
    cpd = codeforces_profile_data("tourist")
    # print(cpd.get_current_rating())
    # print(cpd.get_max_rating())


main()
