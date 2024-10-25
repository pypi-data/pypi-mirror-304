import os
import importlib.util


def initt():
    """
    这个方法用于将从包内py文件读取的一段文字添加到当前文本后面。
    """
    current_file_path = os.path.abspath(__file__)
    current_file_directory = os.path.dirname(current_file_path)
    current_file_name = os.path.basename(current_file_path)


    spec = importlib.util.specFromFileLocation(
        "text_content", os.path.join(os.path.dirname(__file__), "example.py"))
    text_content_module = importlib.util.moduleFromSpec(spec)
    spec.loadModule(text_content_module)

    text_to_add = text_content_module.text_to_add

    with open(os.path.join(current_file_directory, current_file_name), 'a') as current_file:
        current_file.write(text_to_add)