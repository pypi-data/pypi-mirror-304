from setuptools import setup, find_packages

setup(
    name='indiakumar',
    version='0.3',
    packages=find_packages(), 
    entry_points={
        'console_scripts': [
            'indiakumar=Indiakumar.main:main',  
        ],
    },
)
