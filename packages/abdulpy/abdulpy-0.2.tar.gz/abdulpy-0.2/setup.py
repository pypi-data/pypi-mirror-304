from setuptools import setup,find_packages

setup(
    name='abdulpy',
    version='0.2',
    description='A simple library which contains all the programs like simple calculations, loops etc.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    author='Abdul Ahad',
    author_email='noperson883@gmail.com',
    packages=find_packages(),
    install_requires=[],
)