import os
import sys

from setuptools import setup


package = 'dict_trie'
package_name = 'dict-trie'
description = '{}: Basic implementation of a trie.'.format(package_name)
documentation = 'README.md'
license = 'MIT License'
keywords = []

dependencies = []
develop_dependencies = ['pytest', 'tox']
supported = [(2, 7), (3, 3), (3, 4)]
classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering',
]


if sys.version_info < supported[0]:
    raise Exception('{} requires Python {}.{} or higher.'.format(
        package, *supported[0]))

if sys.version_info[:2] == supported[0]:
    dependencies.extend(['argparse', 'importlib'])

# This is quite the hack, but we don't want to import our package from here
# since that's recipe for disaster (it might have some uninstalled
# dependencies, or we might import another already installed version).
distmeta = {}
for line in open(os.path.join(package, '__init__.py')):
    try:
        field, value = (x.strip() for x in line.split('='))
    except ValueError:
        continue
    if field == '__version_info__':
        value = value.strip('[]()')
        value = '.'.join(x.strip(' \'"') for x in value.split(','))
    else:
        value = value.strip('\'"')
    distmeta[field] = value

try:
    with open(documentation) as readme:
        long_description = readme.read()
except IOError:
    long_description = 'See ' + distmeta['__homepage__']

language_string = 'Programming Language :: Python'
classifiers += [
    'License :: OSI Approved :: {}'.format(license),
    'Operating System :: OS Independent',
    language_string,
    '{} :: {}'.format(language_string, supported[0][0]),
    '{} :: {}'.format(language_string, supported[-1][0])] + \
    ['{} :: {}.{}'.format(language_string, *version) for version in supported]

setup(
    name=package_name,
    version=distmeta['__version_info__'],
    description=description,
    long_description=long_description,
    author=distmeta['__author__'],
    author_email=distmeta['__contact__'],
    url=distmeta['__homepage__'],
    license=license,
    platforms=['any'],
    packages=[package],
    install_requires=dependencies,
    tests_require=develop_dependencies,
    classifiers=classifiers,
    keywords=' '.join(keywords)
)
