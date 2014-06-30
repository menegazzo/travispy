from setuptools import setup


setup(
    name='TravisPy',
    version='0.1.1',
    packages=['travispy', 'travispy.entities'],
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
