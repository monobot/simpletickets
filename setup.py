# -*- coding: utf-8 -*-
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='simpletickets',
    version='0.2',
    packages=['simpletickets'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django app to create a ticketting system between '
            'users and staff.',
    long_description=README,
    url='https://github.com/monobot/simpletickets',
    download_url='https://github.com/monobot/simpletickets',
    author='Héctor Alvarez (monobot)',
    author_email='monobot.soft@gmail.com',
    keywords=['django', 'tickets'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
