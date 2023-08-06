# -*- coding: utf-8 -*-
from setuptools import setup
from os import path

# Imports content of requirements.txt into setuptools' install_requires
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


def get_version():
    with open('src/promptoria/pyprompt.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


# Imports content of README.md into setuptools' long_description
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


description='A library to help you focus on your app and not 100% in the prompt. Works great with Jinja2.'

setup(name='promptoria',
      version=get_version(),
      description=description,
      long_description=description,
      keywords='''python3,utility''',
      author='Arturo "Buanzo" Busleiman',
      author_email='buanzo@buanzo.com.ar',
      url='https://github.com/buanzo/promptoria',
      license='MIT',
      zip_safe=False,
      python_requires='>=3.10',
      packages=['promptoria'],
      package_dir={'promptoria': 'src/promptoria'},
      classifiers=[
         'Intended Audience :: Developers',
         'Natural Language :: English',
         'Programming Language :: Python',
         'Programming Language :: Python :: Implementation :: PyPy', ],)
