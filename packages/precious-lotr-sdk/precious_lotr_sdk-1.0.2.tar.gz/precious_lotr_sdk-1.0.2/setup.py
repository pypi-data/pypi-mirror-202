from setuptools import setup, find_packages

setup(
    name='precious_lotr_sdk',
    version='1.0.2',
    description='Python SDK for The Lord of the Rings API',
    author='Suhaib Alfageeh',
    author_email='suhaib@alfadesigned.com',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
