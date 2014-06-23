from setuptools import setup, find_packages

setup(
    name='TravisPy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[x.strip() for x in open('requirements.txt')],

    # metadata for upload to PyPI
    author='Fabio Menegazzo',
    author_email='menegazzo@gmail.com',
    description='Python API for Travis CI.',
    long_description=open('README.md').read(),
    license='GPL',
    keywords='travis ci continuous integration travisci',
    url='http://menegazzo.github.io/travispy/',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',

    ]
)
