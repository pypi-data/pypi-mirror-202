# from distutils.core import setup
from setuptools import setup

with open('README.rst') as file:
    readme = file.read()


setup(
    name='command_fight_game_learning',
    version='2.0.1',
    packages=['CFgame'],
    url='https://testpypi.python.org/pypi/command_fight_game_learning/',
    license='LICENSE.txt',
    long_description='readme.rst',
    author='shuaiegg',
    author_email='jack47.chn@gmail.com'
)

