from data_objects import codeforces_data
from reports import report


class student:
    def __init__(self, name: str, email: str, handles: dict):
        self.name: str = name
        self.email: str = email
        self.handles: dict = handles
        # self.github_info=github(self.handles['github'])
        # self.codechef_info=codechef(self.handles['codechef'])
        self.codeforces_info = codeforces_data.codeforces(self.handles['codeforces'])
        # self.hackerrank_info=hackerrank(self.handles['hackerrank'])
        # self.leetcode_info = leetcode_data.leetcode(self.handles['leetcode'])
        # self.geeks_for_geeks_info = geeks_for_geeks_data.geeks_for_geeks(self.handles['geeks_for_geeks'])
        # self.medium_info=medium(self.handles['medium'])
        # self.stack_overflow_info=stack_overflow_data.stack_overflow(self.handles['stack_overflow'])
        self.complete_info = {
            "name": name,
            "email": email,
            "codeforces": self.codeforces_info,
        }

    def generate_report(self):
        report.report.generate(self.complete_info)
