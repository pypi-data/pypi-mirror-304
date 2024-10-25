import os
import importlib.util
import sys


def initt(pa):
    """
    这个方法用于将从包内文本文件读取的全部内容添加到当前文本后面。
    """
    current_file_path = os.path.abspath(__file__)
    current_file_directory = os.path.dirname(current_file_path)
    current_file_name = os.path.basename(current_file_path)
    
    print("当前Python版本信息：", sys.version_info)
    print("当前Python版本信息：", current_file_directory)
    print("当前Python版本信息：", current_file_name)

    text_to_add = """
    1111
    """

    with open(pa, 'a') as current_file:
        current_file.write(text_to_add)