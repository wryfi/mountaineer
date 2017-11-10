import os
from codecs import open

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'VERSION')) as versionfile:
    VERSION = versionfile.read().strip()


setup(
    name='environty',
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/wryfi/environty',
    license='BSD',
    author='Chris Haumesser',
    author_email='ch@wryfi.net',
    description='manages operations inventory and environments',
    entry_points={
       'console_scripts': [
           'environty-manager=environty.manage:main',
       ],
   },
)
