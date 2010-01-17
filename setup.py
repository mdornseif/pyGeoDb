from setuptools import setup, find_packages

hubarcode = setup(name='pyGeoDb',
    maintainer='Maximillian Dornseif',
    maintainer_email='md@hudora.de',
    # url='http://github.com/hudora/huBarcode',
    version='1.0',
    description='distance calculation based on ZIP codes',
    long_description=long_description,
    classifiers=['License :: OSI Approved :: BSD License',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python'],
    # download_url
    packages=['pygeodb'],
    data_files=[('fonts', ['fonts/cour.pbm', 'fonts/cour.pil', 'fonts/courR08.pbm', 'fonts/courR08.pil',
                           'fonts/courR10.pbm', 'fonts/courR10.pil', 'fonts/courR12.pbm',
                           'fonts/courR12.pil', 'fonts/courR14.pbm', 'fonts/courR14.pil',
                           'fonts/courR18.pbm', 'fonts/courR18.pil', 'fonts/courR24.pbm',
                           'fonts/courR24.pil'])],
    zip_safe=False,
   install_requires=['SQLobject'],
)
