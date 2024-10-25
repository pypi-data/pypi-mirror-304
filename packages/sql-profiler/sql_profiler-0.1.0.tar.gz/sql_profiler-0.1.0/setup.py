# setup.py
from setuptools import setup, find_packages

setup(
    name='sql-profiler',
    version='0.1.0',
    author='Vikas jangid',
    author_email='v7776139@gmail.com',
    description='A package to profile SQL queries and monitor database performance in real-time',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'psutil',
        'mysql-connector-python',  # Updated requirement
    ],
)
