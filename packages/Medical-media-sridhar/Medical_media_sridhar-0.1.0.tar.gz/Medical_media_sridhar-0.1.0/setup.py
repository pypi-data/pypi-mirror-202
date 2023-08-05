from setuptools import setup, find_packages
import os

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='Medical_media_sridhar',
    version='0.1.0',
    author='Sridhar',
    author_email='dcsvsridhar@gmail.com',
    description='Medical_media is like a Health Condition checking tool',
    packages=find_packages(),
    url='https://git.selfmade.ninja/SRIDHARDSCV/bmi_calculater_python_project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'Medical_media=main.main:main',
        ],
    },
)