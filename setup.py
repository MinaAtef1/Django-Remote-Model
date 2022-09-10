from setuptools import setup, find_packages
from glob import glob


setup(
    name='django_remote_model',
    version='0.1.6',
    license='MIT',
    author="Mina Atef",
    author_email='mina.atef0@gmail.com',
    packages=['django_remote_model.remote_model','django_remote_model.provider'],
    package_dir={'django_remote_model.remote_model':'./django_remote_model/remote_model','django_remote_model.provider':'./django_remote_model/provider'},
    url='https://github.com/minaaaatef/Django-Remote-Model',
    keywords='django remote model rest api',
)