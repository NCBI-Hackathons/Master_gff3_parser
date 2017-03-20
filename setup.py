from setuptools import setup
import glob
import os

with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if not x.startswith("#")]

from cli import __version__, _program

setup(name=_program,
      version=__version__,
      packages=['cli'],
      description='GFF Parser',
      url='https://github.com/NCBI-Hackathons/Master_gff3_parser',
      author='NCBI-Hackathons',
      license='MIT',
      entry_points="""
      [console_scripts]
      {program} = cli.command:main
      """.format(program = _program),
      keywords=[],
      tests_require=['pytest', 'coveralls'],
      zip_safe=False)
