from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='flixy2app',
    version='0.2.1',
    author='SKbarbon',
    description='A UI-Builder that helps programmers build the front-end without codding it.',
    long_description=long_description,
    url='https://github.com/SKbarbon/flixy',
    install_requires=["flet", "requests", "PyInstaller"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],
)