from setuptools import setup, find_packages

setup(
    name='Ilyass', 
    version='1.3',
    packages=find_packages(),
    install_requires=[
        'requests',
        'uuid',
        'user_agent'
        
    ],
    author='ILYASS MOROX',
    author_email='ilyassvv@gmail.com',
    description='Best library to check Hotmail email if is available',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    url='https://t.me/n1z1n',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)