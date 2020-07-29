from string import Template

from helper_methods import help


class header:
    @staticmethod
    def generate(name, email):
        template_name = "header.tmpl"
        template_structure = help.load_template(template_name)
        template = Template(template_structure)
        substitute_dict = {
            "name": name,
        }
        template = template.substitute(substitute_dict)
        return template
