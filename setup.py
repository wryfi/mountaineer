import os
from codecs import open

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'VERSION')) as versionfile:
    VERSION = versionfile.read().strip()


setup(
    name='mountaineer',
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/wryfi/mountaineer',
    license='BSD',
    author='Chris Haumesser',
    author_email='ch@wryfi.net',
    description='manages operations inventory and environments',
    # entry_points={
    #    'console_scripts': [
    #        'mountaineer-manager=mountaineer.manage:main',
    #    ],
    # },
)
