from setuptools import setup,find_packages

setup(
    name='goby_sdk',
    version='1.0.7',
    description='A Python SDK for Goby, Visit for details: https://www.exp-9.com/category-20.html',
    author='siberia',
    author_email='siberiah0h@gmail.com',
    project_description='这是一个非官方版的GOBY SDK , 基于goby-x64-2.4.5-Community 进行开发,用于解决企业快速嵌入goby扫描引擎的问题, SDK文档详情请关注: https://www.exp-9.com/category-20.html 或者 https://github.com/siberiah0h/goby_sdk_for_python',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
)