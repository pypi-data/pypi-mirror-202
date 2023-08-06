from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as readme:
    with codecs.open(os.path.join(here, "CHANGELOG.md"), encoding="utf-8") as changelog:
        LONG_DESCRIPTION = readme.read() + '\n\n\n' + changelog.read()


VERSION = '0.0.6'
DESCRIPTION = 'Write Simple and Quick Python GUI Application'
KEYWORDS = ['gui', 'clera', 'simple', 'simplegui', 'pyside', 'pyside6']

# LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
]

# Setting up
setup(
    name="clera",
    version=VERSION,
    author="Erasmus A. Junior",
    author_email="eirasmx@pm.me",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    licence='MIT',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['PySide6'],
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    py_modules=['clera']
)

