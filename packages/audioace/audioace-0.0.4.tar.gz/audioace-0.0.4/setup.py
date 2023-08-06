from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

VERSION = '0.0.4'
DESCRIPTION = 'Downloads your favourite music'

# Setting up
setup(
    name="audioace",
    author="Vikranth",
    version=VERSION,
    author_email="<vikrantht32@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url = "https://github.com/VikranthMaster/AudioAce.git",
    project_urls = {
        "Bug Tracker" : "https://github.com/VikranthMaster/AudioAce/issues"
    },
    packages=find_packages(),
    install_requires=['pytube', 'pywhatkit', 'requests', 'moviepy', 'spotipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)