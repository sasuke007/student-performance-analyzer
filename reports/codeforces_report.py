from string import Template

from data_objects.codeforces_data import codeforces
from helper_methods import help


class codeforces_report:

    @staticmethod
    def generate(codeforces_info):
        template_name = "codeforces.tmpl"
        template_structure = help.load_template(template_name)
        template = Template(template_structure)
        questions_info = codeforces_info.questions
        substitute_dict = {
            "rank": codeforces_info.rank,
            "profile_link": codeforces_info.student_profile_link,
            "handle": codeforces_info.student_handle,
            "current_rating": codeforces_info.current_rating,
            "max_rating": codeforces_info.max_rating,
            "contribution": codeforces_info.contribution,
            "questions_solved": codeforces_info.questions_solved,
        }
        count = 1
        for name, link in questions_info.items():
            number = str(count)
            name_placeholder = "name_" + number
            link_placeholder = "link_" + number
            substitute_dict[name_placeholder] = name
            substitute_dict[link_placeholder] = link
            count += 1
            if count > 12:
                break
        template = template.substitute(substitute_dict)
        return template


def main():
    cfi = codeforces("AnestheticCoder")
    codeforces_report.generate(cfi)


if __name__ == "__main__":
    main()
