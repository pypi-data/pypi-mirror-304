# coding:utf-8


from setuptools import setup, find_packages
from pyco_types import __version__

# 版本信息
version = __version__

setup(
    name="pyco-types",  # 这里是pip项目发布的名称
    version=version,  # 版本号，数值大的会优先被pip
    keywords=[
        "pyco-types", "datetime", "regex-patten",
        "converter", "type-formatter"
    ],
    description="pyco types: Flexible Extensionable Python Types with Converter",
    long_description=(
        "pyco types: Flexible Extensionable Python Types with Converter"
    ),
    license='GNU LGPLv3',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],
    url="https://github.com/vmicode/pyco-types",
    author="dodoru",
    author_email="dodoru@foxmail.com",
    packages=find_packages(exclude=('tests', 'tests.*', 'docs', 'examples', '*.tests')),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "python-dateutil>=2.4.0",
        "orjson>=3.10.0",
    ]
)
