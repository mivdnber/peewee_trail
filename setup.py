import os
import sys
import warnings
from setuptools import setup

setup(
    name='peewee_trail',
    version='0.1',
    description='Audit trails for peewee using PostgreSQL temporal tables',
    long_description=open('README.rst', 'rt').read(),
    author='Michiel Van den Berghe',
    author_email='michiel.vdb@gmail.com',
    url='http://github.com/mivdnber/peewee_trail',
    packages=['peewee_trail'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['peewee', 'psycopg2']
)
