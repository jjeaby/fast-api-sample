from os import path


def file_path(file):
    """
    current file path return
    :param file:
    :return: current file path
    """
    _file_path = path.dirname(path.dirname(path.dirname(path.abspath(file))))
    return _file_path


def root_path():
    """
    project root path return
    :return: project root path
    """
    return path.dirname(path.dirname(path.abspath(__file__)))
