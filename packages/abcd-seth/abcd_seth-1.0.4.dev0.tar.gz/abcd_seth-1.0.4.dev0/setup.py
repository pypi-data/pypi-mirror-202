from setuptools import setup, find_packages

setup(
    name='abcd_seth',
    version='1.0.4-dev',
    description='Shared models for microservices',
    author='Daniyar Auezkhan',
    author_email='nurovich14@gmail.com',
    packages=find_packages(exclude=('tests',)),
    install_requires=[

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
