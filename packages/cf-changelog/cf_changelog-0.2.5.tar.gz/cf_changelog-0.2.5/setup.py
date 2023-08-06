#!/usr/bin/env python

from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='cf_changelog',
      long_description=long_description,
      long_description_content_type='text/markdown',
      version='0.2.5',
      description='Conflict-Free Changelog manager',
      author='Paweł Sałek',
      author_email='salekpawel@gmail.com',
      url='https://gitlab.com/salekpawel/cf_changelog',
      packages=['cf_changelog', ],
      license="MIT",
      install_requires=[
        'GitPython >= 3.1.0',
        'pyyaml >= 6.0',
        'schema >= 0.7.0',
      ],
      entry_points={
        'console_scripts': [
            'cf_changelog = cf_changelog:main',
        ]
      }
     )