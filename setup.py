# -*- encoding: utf-8 -*-

import os.path
from setuptools import setup


# Utility function to read the README file.
# Taken from setuptools examples on pythonhosted.org
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "mysql_modelstatus",
    version = "0.0.1pa1",
    author = "Radosław 'warran' Warzocha",
    author_email = "radoslaw.warzocha@gmail.com",
    description = ("Mixin for including status in the SQLAlchemy Models. Status definition can be given as a `dict` "
                   "type class attribute. Definition can restrict certain status transition and give the default"
                   "value."),
    long_description=read('README.md'),
    keywords = "sqlalchemy model mixin status",
    url = "https://github.com/warran/sqlalchemy_modelstatus",
    packages=['sqlalchemy_modelstatus'],
    license = "GNU LGPL",

    install_requires=[
        'enum34==1.1.6;python_version<"3.4"',
        'SQLAlchemy==1.1.7'
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2'
        'Programming Language :: Python :: 2.7'
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.4'
        'Programming Language :: Python :: 3.5'
        'Programming Language :: Python :: 3.6'
        'Topic :: Software Development'
        ],
)
