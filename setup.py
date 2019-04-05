import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf_nested_relations',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A library for crud of nested relations',
    long_description=README,
    # url='https://www.example.com/',
    # author='Your Name',
    # author_email='yourname@example.com',
    # classifiers=[
    #     'Environment :: Web Environment',
    #     'Framework :: Django',
    #     'Framework :: Django :: X.Y',  # replace "X.Y" as appropriate
    #     'Intended Audience :: Developers',
    #     'License :: OSI Approved :: BSD License',  # example license
    #     'Operating System :: OS Independent',
    #     'Programming Language :: Python',
    #     'Programming Language :: Python :: 3.5',
    #     'Programming Language :: Python :: 3.6',
    #     'Topic :: Internet :: WWW/HTTP',
    #     'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    # ],
)