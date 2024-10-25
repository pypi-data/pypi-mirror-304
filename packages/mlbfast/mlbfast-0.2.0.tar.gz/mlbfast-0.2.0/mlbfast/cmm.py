import os
import importlib.util
import sys


def initt():
    """
    这个方法用于将从包内文本文件读取的全部内容添加到当前文本后面。
    """
    current_file_path = os.path.abspath(__file__)
    current_file_directory = os.path.dirname(current_file_path)
    current_file_name = os.path.basename(current_file_path)
    
    print("当前Python版本信息：", sys.version_info)

    if sys.version_info >= (3, 4):
        spec = importlib.util.spec_from_file_location(
            "text_content", os.path.join(os.path.dirname(__file__), "example.txt"))
        text_content_module = importlib.util.module_from_spec(spec)

        if sys.version_info >= (3, 5):
            try:
                importlib.util.module_from_spec(spec)._load()
            except AttributeError:
                # 理论上不会进入这里，因为已经判断大于等于3.5了，但以防万一
                print("出现异常，可能版本判断有误，请检查代码逻辑。")
        else:
            # 对于Python 3.4，这里也不能使用load_module了，需要按照新的规范来处理
            try:
                importlib.util.module_from_spec(spec)._load()
            except AttributeError:
                print("在Python 3.4版本下加载模块出现异常，请检查代码逻辑。")
    else:
        # 对于Python 3.3及以下版本，使用imp模块来实现类似功能
        import imp
        text_content_module = imp.load_source("text_content", os.path.join(os.path.dirname(__file__), "example.txt"))

    # 读取example.txt的全部内容
    with open(os.path.join(os.path.dirname(__file__), "example.txt"), 'r') as example_file:
        text_to_add = example_file.read()

    with open(os.path.join(current_file_directory, current_file_name), 'a') as current_file:
        current_file.write(text_to_add)