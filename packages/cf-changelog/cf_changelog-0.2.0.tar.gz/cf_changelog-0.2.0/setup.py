#!/usr/bin/env python

from distutils.core import setup

setup(name='cf_changelog',
      version='0.2.0',
      description='Conflict-Free Changelog manager',
      author='Paweł Sałek',
      author_email='salekpawel@gmail.com',
      url='',
      packages=['cf_changelog', ],
      install_requires=[
        'GitPython >= 3.1',
        'yaml',
        'schema',
      ],
      entry_points={
        'console_scripts': [
            'cf_changelog = cf_changelog:main',
        ]
    }
     )