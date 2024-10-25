# setup.py
from setuptools import setup, find_packages

setup(
    name='TurboTalk_VAI',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition',
        'pyttsx3',
        'colorama',
        # Add any other dependencies your module needs
    ],
)
