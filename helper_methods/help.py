import os

import requests


def strip_string(input_str, token=" "):
    input_str = str(input_str)
    input_str = input_str.strip('\n')
    input_str = input_str.strip(token)
    input_str = input_str.strip('\n')
    return input_str


def split_string(input_str, token='/'):
    input_str = strip_string(input_str)
    # print(input_str)
    input_str = input_str.split(token)
    # print(input_str)
    for i in range(len(input_str)):
        input_str[i] = strip_string(input_str[i])
    return input_str


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def send_request(link):
    html = None
    try:
        html = requests.get(link)
    except Exception as ex:
        print(ex)
    finally:
        return html


def write_data_to_file(data, path):
    file = open(path, "w", encoding="utf-8")
    file.write(data)
    file.close()


def read_file(path):
    file = open(path, "r", encoding="utf-8")
    data = file.read()
    file.close()
    return data


def load_template(template_name):
    root_path = "E:\\PyCharm\\Student Performance Analyzer"
    path = os.path.join(root_path, "templates", template_name)
    template = read_file(path)
    return template


def relocate_file(source, destination):
    os.rename(source, destination)
