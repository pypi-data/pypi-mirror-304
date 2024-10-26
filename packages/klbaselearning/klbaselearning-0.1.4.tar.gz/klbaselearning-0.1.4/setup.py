import setuptools
from setuptools import setup, find_packages

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='klbaselearning',  # 替换为你项目的名称
    version='0.1.4',
    include_package_data=True,
    author='kkl',
    author_email='kkl2@gmail.com',
    description='A package with machine learning tasks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),  # 自动发现项目中的包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
    ],
)
