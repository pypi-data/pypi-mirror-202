from setuptools import setup,find_packages

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='goby_sdk',
    version='1.0.9',
    description='A Python SDK for Goby, Visit for details: https://www.exp-9.com/category-20.html',
    author='siberia',
    author_email='siberiah0h@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/siberiah0h/goby_sdk_for_python",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
)