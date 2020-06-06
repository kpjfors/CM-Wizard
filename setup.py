from setuptools import setup

setup(
    name='CM-Wizard',
    version='2.0',
    packages=['app', 'app.toolbox', 'toolbox'],
    package_dir={'': 'app'},
    url='https://github.com/kpjfors/',
    license='GPL-3',
    author='Johan Fors',
    author_email='johanfors93@gmail.com',
    description='Tools for managing postings on CardMarket.'
)


