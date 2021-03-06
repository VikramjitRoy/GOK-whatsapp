#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages

import platform

deps = ['rivescript','python-dateutil', 'argparse', 'python-axolotl>=0.1.7', 'pillow','pymongo','yowsup2']

if platform.system().lower() == "windows":
    deps.append('pyreadline')
else:
    try:
        import readline
    except ImportError:
        deps.append('readline')

setup(
    name='GOK-whatsapp',
    #version=yowsup.__version__,
    url='https://github.com/VikramjitRoy/GOK-whatsapp/',
    license='GPL-3+',
    author='Tarek Galal',
    tests_require=[],
    install_requires = deps,
    #scripts = ['yowsup-cli'],
    #cmdclass={'test': PyTest},
    author_email='tare2.galal@gmail.com',
    
    description='A WhatsApp python library',
    #long_description=long_description,
    packages= find_packages(),
    include_package_data=True,
    platforms='any',
    #test_suite='',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        #'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    #extras_require={
    #    'testing': ['pytest'],
    #)  
)
