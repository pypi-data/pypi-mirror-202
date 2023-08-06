from setuptools import setup, find_packages

setup(
    name='magpy_nc',
    version='2.0.1',
    license='MIT License',
    long_description='readme',
    author='Leonardo Mota',
    author_email='dev.lamota@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'requests'
    ],
)
