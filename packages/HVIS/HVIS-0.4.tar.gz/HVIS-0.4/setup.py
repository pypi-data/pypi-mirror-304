
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='HVIS',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'requests',
        'user-agent',
        'base64',
    ],
    description='A library for extracting text from CAPTCHA images, easy to use for developers.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Twinsszi',
    author_email='adhm90879@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
