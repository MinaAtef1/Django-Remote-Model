from setuptools import setup, find_packages
from glob import glob


setup(
    name='django_remote_model',
    version='0.1',
    license='MIT',
    author="Mina Atef",
    author_email='mina.atef0@gmail.com',
    packages=['dynamic_remote_model','dynamic_remote_model.provider'],

    url='https://github.com/minaaaatef/Django-Remote-Model',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],


)