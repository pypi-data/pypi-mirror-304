from setuptools import setup, find_packages

setup(
    name='mlbfast',  # 库的名称
    version='0.3.0',  # 版本号
    keywords=['pip', 'wxw'],
    description='A library for wxw',  # 简要描述
    long_description="Includes some ways to work with pictures",

    author='xxx',  # 作者名字
    author_email='xxxx@xxx.com',  # 作者邮箱
    url='https://github.com/xxx/xxxx',  # 项目的URL

    packages=find_packages(),  # 需要打包的目录列表
    platforms="any",
    install_requires=[]  # 这个项目依赖的第三方库
)