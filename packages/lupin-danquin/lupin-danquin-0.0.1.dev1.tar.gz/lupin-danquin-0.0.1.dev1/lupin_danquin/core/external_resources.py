import codecs
import os


def read_begining_of_file() -> str:
    result = ""
    path = os.path.dirname(__file__) + os.sep + ".." + os.sep + "assets" + os.sep
    with codecs.open(path + "BeginingOfFile.md", encoding="utf-8") as f:
        result = f.read()
    return result


def read_end_of_file() -> str:
    result = ""
    path = os.path.dirname(__file__) + os.sep + ".." + os.sep + "assets" + os.sep
    with codecs.open(path + "EndOfFile.md", encoding="utf-8") as f:
        result = f.read()
    return result
