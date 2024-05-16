from setuptools import setup, find_packages

setup(
    name='thechain',
    version='0.0.0',
    packages=find_packages(),
    description='The simple POW block chain',
    long_description=open('README.md').read(),
    author='bclin',
    author_email='mbb200291@gmail.com',
    url='https://github.com/mbb200291/thechain',
    install_requires=open('thechain/requirements.txt').readlines(),
)
