import os
import importlib.util
import sys


def initt():
    """
    这个方法用于将从包内py文件读取的一段文字添加到当前文本后面。
    """
    current_file_path = os.path.abspath(__file__)
    current_file_directory = os.path.dirname(current_file_path)
    current_file_name = os.path.basename(current_file_path)

    if sys.version_info >= (3, 4):
        spec = importlib.util.spec_from_file_location(
            "text_content", os.path.join(os.path.dirname(__file__), "example.py"))
        text_content_module = importlib.util.module_from_spec(spec)

        # 在Python 3.5及以上版本，使用exec_module方法加载模块
        if sys.version_info >= (3, 5):
            spec.exec_module(text_content_module)
        else:
            spec.load_module(text_content_module)

    else:
        # 对于Python 3.3及以下版本，使用imp模块来实现类似功能
        import imp
        text_content_module = imp.load_source("text_content", os.path.join(os.path.dirname(__file__), "example.py"))

    text_to_add = text_content_module.text_to_add

    with open(os.path.join(current_file_directory, current_file_name), 'a') as current_file:
        current_file.write(text_to_add)