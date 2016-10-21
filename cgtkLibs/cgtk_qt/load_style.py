# coding=utf8


def load_style(qss_file):
    f = open(qss_file, 'r')
    data = f.read()
    data.strip('\n')
    return data
