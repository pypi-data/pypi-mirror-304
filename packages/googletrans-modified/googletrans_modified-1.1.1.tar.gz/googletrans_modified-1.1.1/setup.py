#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import re

from setuptools import find_packages, setup


def __get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass


def __get_version():
    init_py = __get_file(os.path.dirname(__file__), 'googletrans', '__init__.py')
    pattern = r"{0}\W*=\W*'([^']+)'".format('__version__')
    version, = re.findall(pattern, init_py)
    return version


def __get_description():
    init_py = __get_file(os.path.dirname(__file__), 'googletrans', '__init__.py')
    pattern = r'"""(.*?)"""'
    description, = re.findall(pattern, init_py, re.DOTALL)
    return description


def __get_readme():
    return __get_file(os.path.dirname(__file__), 'README.rst')


def install():
    setup(
        name='googletrans-modified',
        version=__get_version(),
        description=__get_description(),
        long_description=__get_readme(),
        license='MIT',
        author='Hayk Serobyan',
        author_email='hayk.serobyan.89@gmail.com',
        url='https://github.com/HaykSerobyan-89/py-googletrans-modified',
        classifiers=[
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: MacOS :: MacOS X',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Programming Language :: Python :: 3.13',
        ],
        packages=find_packages(exclude=['docs', 'tests']),
        keywords='google translate translator',
        install_requires=['httpx[http2]>=0.23', ],
        python_requires='>=3.6',
        tests_require=['pytest', 'coveralls', ],
        scripts=['translate']
    )


if __name__ == "__main__":
    install()
