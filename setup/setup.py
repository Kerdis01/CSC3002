####-RUN 'MAKE' TO INSTALL DEPENDENCIES-####

from setuptools import setup, find_packages

setup(
    name='csc3002',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'tflite-runtime'
        'numpy'
    ]
)