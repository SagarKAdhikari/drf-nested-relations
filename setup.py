import os
from setuptools import find_packages, setup
from nested_relations import VERSION
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf-nested-relations',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  
    description='An extension of django rest framework that allows writing nested relations',
    long_description=README,
    url='https://github.com/SagarKAdhikari/drf-nested-relations',
    author='Sagar Adhikari',
    author_email='ska80117@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 2.0 ',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
