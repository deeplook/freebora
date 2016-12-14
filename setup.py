"""
Freebora: fetch free ebooks from O'Reilly online shop.
"""

from setuptools import find_packages, setup
import distutils.core

from freebora.version import __version__


class PyTest(distutils.core.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py', 'tests'])
        raise SystemExit(errno)


def get_dependencies(filename):
    return open(filename).read().strip().split('\n')


setup(
    name='freebora',
    version=__version__,
    url='https://github.com/deeplook/freebora/',
    license='GPL3',
    author='Dinu Gherman',
    author_email='gherman@darwin.in-berlin.de',
    description=__doc__,
    packages=['freebora'], # find_packages(exclude='tests'),
    entry_points={
        'console_scripts': ['freebora=freebora.__main__:main']
    },
    zip_safe=False,
    platforms='any',
    install_requires=get_dependencies('requirements.txt'),
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: System :: Archiving',
        'Topic :: Utilities',
    ]
)
