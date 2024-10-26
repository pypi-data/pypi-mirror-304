# etl_package/setup.py

# swiftetl/setup.py

# swiftetl/setup.py

from setuptools import setup, find_packages

setup(
    name='swiftetl',  # PyPI package name
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    description='A simple ETL pipeline package for data extraction, transformation, and loading into SQLite.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Required for Markdown README
    author='Harsh Jain',
    author_email='jharshit61@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
