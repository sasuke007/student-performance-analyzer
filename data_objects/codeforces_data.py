import extract.codeforces.codeforces_profile_data as codeforces_profile
import extract.codeforces.codeforces_questions_data as codeforces_questions


class codeforces:
    # This class will contain all the data retrieved from codeforces and methods required
    # to manipulate and extract that data
    def __init__(self, handle):
        profile = codeforces_profile.codeforces_profile_data(handle)
        questions_profile = codeforces_questions.codeforces_questions_data(handle)
        self.rank = profile.get_rank()
        self.current_rating = profile.get_current_rating()
        self.max_rating = profile.get_max_rating()
        self.contribution = profile.get_contribution()
        self.friends = profile.get_friends()
        self.registered_on = profile.get_registered_on()
        self.questions = questions_profile.get_questions_list()
        self.student_profile_link = profile.get_student_profile_link()
        self.student_handle = handle
        self.questions_solved = len(self.questions)
        # self.display()

    def display(self):
        print("rank ", self.rank)
        print("current_rating : ", self.current_rating)
        print("max_rating : ", self.max_rating)
        print("contribution : ", self.contribution)
        print("friends : ", self.friends)
        print("registered_on : ", self.registered_on)
        print("question info")
        for name, link in self.questions.items():
            print(name, link)


def main():
    cf = codeforces("AnestheticCoder")


if __name__ == "__main__":
    main()
