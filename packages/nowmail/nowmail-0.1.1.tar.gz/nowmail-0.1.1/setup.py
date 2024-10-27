from setuptools import setup, find_packages

setup(
    name="nowmail",
    version="0.1.1",
    description="A powerful library for creating and managing temporary email accounts",
    long_description=open("ReadME(en).md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="devnu",
    author_email="mma140305@gmail.com",
    url="https://github.com/noon05/nowmail",
    packages=find_packages(include=["nowmail", "nowmail.*"]),
    include_package_data=True, 
    install_requires=[
       
    ],
    python_requires='>=3.6',
)