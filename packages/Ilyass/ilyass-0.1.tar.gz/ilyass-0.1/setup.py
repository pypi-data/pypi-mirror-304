# setup.py

from setuptools import setup, find_packages

setup(
    name="Ilyass",
    version="0.1", 
    description="Library to check Hotmail email availability",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Ilyass",
    author_email="ilyasssr120@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)
