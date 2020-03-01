import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='cloc',
    version='0.0.8',
    packages=find_packages(exclude=['examples']),
    include_package_data=True,
    description='Command Line Object Chaining (cloc) - Modern cli framework for simple and complex cli applications',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://www.github.com/tannerburns/cloc',
    author='Tanner Burns',
    author_email='tjburns102@gmail.com',
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
)