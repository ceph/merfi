import re

module_file = open("merfi/__init__.py").read()
metadata = dict(re.findall("__([a-z]+)__\s*=\s*'([^']+)'", module_file))
long_description = open('README.rst').read()

from setuptools import setup, find_packages

setup(
    name = 'merfi',
    description = 'Signs release files',
    packages = find_packages(),
    author = 'Alfredo Deza',
    author_email = 'alfredo@deza.pe',
    scripts = ['bin/merfi'],
    install_requires = ['tambo>=0.1.0'],
    version = metadata['version'],
    url = 'http://github.com/alfredodeza/merfi',
    license = "MIT",
    zip_safe = False,
    keywords = "rpm-sign, gpg, release, binaries",
    long_description = long_description,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    tests_require=[
        'pytest'
    ]
)
