from setuptools import setup,find_packages

setup(
    name='goby_sdk',
    version='1.0.8',
    description='A Python SDK for Goby, Visit for details: https://www.exp-9.com/category-20.html',
    author='siberia',
    author_email='siberiah0h@gmail.com',
    project_description='This is an unofficial version of the GOBY SDK, developed based on goby-x64-2.4.5-Community to address the problem of rapid integration of the GOBY scanning engine into enterprise systems. For more details about the SDK documentation, please visit https://www.exp-9.com/category-20.html or https://github.com/siberiah0h/goby_sdk_for_python.',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
)