from datetime import date
import sys
from setuptools import setup, find_packages
# pylint: disable = relative-import
import obsutil

pkgs = find_packages()

if __name__ == '__main__':
    name = 'obsutil'

    requirements = ['esdk-obs-python']

    setup(
        name=name,
        version='1.0.4',
        description='hw modelarts obs utils',
        # long_description='',
        # author='Taichu platform team',
        # author_email='noreply@noreply.com',
        python_requires=">=3.6.0",
        url='',
        # keywords='Serving Deep Learning Inference AI',
        packages=pkgs,
        install_requires=requirements,
        include_package_data=True,
        # license='Apache License Version 2.0'
    )
