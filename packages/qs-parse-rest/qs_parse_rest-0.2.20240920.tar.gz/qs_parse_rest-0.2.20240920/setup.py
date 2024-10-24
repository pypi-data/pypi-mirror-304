import os
from setuptools import setup, Command
from unittest import TextTestRunner, TestLoader


class TestCommand(Command):
    '''Run test suite using `python setup.py test `'''
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        '''Run test suite in parse_rest.tests'''
        tests = TestLoader().loadTestsFromNames(['parse_rest.tests'])
        t = TextTestRunner(verbosity=1)
        t.run(tests)

# python setup.py sdist bdist_wheel
# pip install twine
# twine upload dist/*
setup(
    name='qs-parse-rest',
    version='0.2.20240920',
    description='A client library for Parse.com\'.s REST API',
    url='https://github.com/milesrichardson/ParsePy',
    packages=['parse_rest'],
    package_data={"parse_rest": [os.path.join("cloudcode", "*", "*")]},
    install_requires=['six'],
    maintainer='Miles Richardson',
    maintainer_email='miles.richardson@gmail.com',
    cmdclass={'test': TestCommand},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.12",
    ]
)
