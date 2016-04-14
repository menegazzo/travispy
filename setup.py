from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        args = ['travispy']
        if self.pytest_args:
            args.insert(0, self.pytest_args)
        errno = pytest.main(args)
        sys.exit(errno)


setup(
    name='TravisPy',
    version='0.3.5',
    packages=['travispy', 'travispy.entities'],
    install_requires=[x.strip() for x in open('requirements.txt')],

    # metadata for upload to PyPI
    author='Fabio Menegazzo',
    author_email='menegazzo@gmail.com',
    description='Python API for Travis CI.',
    long_description=open('README.rst').read(),
    license='GPL',
    keywords='travis ci continuous integration travisci',
    url='https://github.com/menegazzo/travispy',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    # tests
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
