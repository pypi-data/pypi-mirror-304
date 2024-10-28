# -*- coding:utf-8 -*-

'''
For pypi
'''

from setuptools import find_packages, setup

desc = ('Flexible, extensible Web CMS framework built on Tornado,'
        'compatible with Python 3.7 and above.')
setup(
    name='slwork',
    version='0.0.1',
    keywords=['slwork'],
    description=desc,
    long_description=''.join(open('README.rst').readlines()),
    license='MIT License',

    url='https://bukun.coding.net/p/dev/d/slwork/git',
    author='bukun',
    author_email='bukun@osgeo.cn',

    packages=find_packages(
        include=('slwork_function',),
        # exclude=('slw')
        ),
    include_package_data=True,

    platforms='any',
    zip_safe=True,
    install_requires=['pandas','numpy','pathlib',
                     'numpy',],

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
