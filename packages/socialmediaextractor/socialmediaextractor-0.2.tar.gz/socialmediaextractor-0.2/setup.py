from setuptools import setup, find_packages

setup(
    name='socialmediaextractor',
    version='0.2',
    description='A library to extract social media links from websites',
    author='Md Irfan Ali',
    author_email='irfanali29@hotmail.com',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
)



