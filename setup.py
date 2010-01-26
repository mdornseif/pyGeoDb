import codecs
from setuptools import setup, find_packages

hubarcode = setup(name='pyGeoDb',
    maintainer='Maximillian Dornseif',
    maintainer_email='md@hudora.de',
    url='http://github.com/mdornseif/pyGeoDb',
    version='1.2',
    description='distance calculation based on ZIP codes and map generation',
    long_description=open('README.rst').read().decode('utf-8'),
    classifiers=['License :: OSI Approved :: BSD License',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python'],
    # download_url
    packages=['pygeodb'],
    scripts=['plz_draw']
)
