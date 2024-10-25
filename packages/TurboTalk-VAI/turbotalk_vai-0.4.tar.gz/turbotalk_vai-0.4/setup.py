# setup.py
from setuptools import setup, find_packages

setup(
    name='TurboTalk_VAI',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition',
        'pyttsx3',
        'colorama',
        'TurboTalk_Custom',
        # Add any other dependencies your module needs
    ],
)
