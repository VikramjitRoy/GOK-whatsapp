#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import platform

deps = ['python-dateutil', 'argparse', 'python-axolotl>=0.1.7', 'pillow','yowsup2','rivescript','pymongo','datetime']

if platform.system().lower() == "windows":
    deps.append('pyreadline')
else:
    try:
        import readline
    except ImportError:
        deps.append('readline')

setup(
    name='GOK-whatsapp',
    version=0.1,
    url='http://github.com/VikramjitRoy/GOK-whatsapp/',
    license='GPL-3+',
    author='Vikramjit Roy,Abhilash Verma',
    tests_require=[],
    install_requires = deps,
    
    #cmdclass={'test': PyTest},
    author_email='vikram.jee2012@gmail.com,royron22@gmail.com',
    description='A WhatsApp bot for GOk',
    #long_description=long_description,
    packages= find_packages(),
    include_package_data=True,
    platforms='any',
    #test_suite='',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: Beta',
        'Natural Language :: English',
        #'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    #extras_require={
    #    'testing': ['pytest'],
    #}
)
