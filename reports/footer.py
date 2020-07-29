from string import Template

from helper_methods import help


class footer:

    @staticmethod
    def generate():
        template_name = 'footer.tmpl'
        template_structure = help.load_template(template_name)
        template = Template(template_structure)
        substitute_dict = {}
        template = template.substitute(substitute_dict)
        return template


def main():
    print(footer.generate())


if __name__ == "__main__":
    main()
