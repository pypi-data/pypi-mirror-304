

from setuptools import setup, find_packages

setup(
    name='CodEasy',
    version='0.1',
    description='A package to auto-generate boilerplate code for common programming needs.',
    author='Aryan Shanker Saxena',
    author_email='aryan11234567890@gmail.com',
    url='https://github.com/Aryan11234567890/CodEasy',  # Your GitHub repo URL
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
)
