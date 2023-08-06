from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Downloads your favourite music'
LONG_DESCRIPTION = 'A package that allows to download your favourite music'

# Setting up
setup(
    name="audioace",
    author="Vikranth",
    author_email="<vikrantht32@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pytube', 'pywhatkit', 'requests', 'moviepy', 'spotipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)