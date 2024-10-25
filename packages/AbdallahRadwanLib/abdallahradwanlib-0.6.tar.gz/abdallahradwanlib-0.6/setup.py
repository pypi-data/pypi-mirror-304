import setuptools
from setuptools import setup

setup(
    name='AbdallahRadwanLib',
    version='0.6',    
    description='My First Package for Python Projects with PyPI Package - October 2024',  
    package_dir={"": "app"},
    packages=setuptools.find_packages(where="app"),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/abdorado1984/AbdallahPackage',
    author='Abdallah Radwan',
    author_email='AbdallahRadwan2011@gmail.com',    
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",        
    ],       
)

# packages=['arUtilities'],
