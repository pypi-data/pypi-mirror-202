from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.0'
DESCRIPTION = 'PyLanguageEasy'
LONG_DESCRIPTION = """
Easy Python Language

Helps you to make python easier and more understandable

some example:
you can change color of text, print on same line, delete and re-output again and many others, image process.
It makes making 2d game easier you can scroll background with just one line of code, check user input, collide and many others.
put image, and many others
calculate any number like using calculate(\"2+2*4/5\") and builtin bot

turn text to speech and speech to text just on one of code

some function

Bot()
calculate()
re_output()
resizeImage() 
and many others

join on discord (Shiva321#1848) for update and help.


"""

# Setting up
setup(
    name="PyLanguageEasy",
    version=VERSION,
    author="Developer HelloUsers",
    author_email="duartesaopedrocat1@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pygame", "Pillow", "pyttsx3", "SpeechRecognition", "datetime", "keyboard", "termcolor"],
    keywords=['python', 'Pylan', 'pylan', 'EasyPython', 'EasyPyLan', "easypylan", "pygame", "game", "image"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)