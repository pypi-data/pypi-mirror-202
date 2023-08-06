# -*- coding:utf-8 -*-
# from distutils.core import setup
from setuptools import find_packages
from setuptools import setup
from pathlib import Path

setup(
    name='baselib',
    version="1.0.7.1",
    description='base common lib for python',
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author='coreylam',
    author_email='coreylam@163.com',
    url='https://github.com/coreylam/base_common_lib',
    license='GPL',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],
    python_requires=">=2.7",
)
