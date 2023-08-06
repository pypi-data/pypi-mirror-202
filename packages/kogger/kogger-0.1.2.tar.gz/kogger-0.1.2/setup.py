"""
@author: bochengz
@date: 2023/04/12
@email: bochengzeng@bochengz.top
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kogger",
    version="0.1.2",
    license='MIT',
    author="bochengz",
    author_email="bochengzeng@bochengz.top",
    description="A very simple logger.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zengbocheng/kogger.git",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)