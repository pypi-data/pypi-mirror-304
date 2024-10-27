from setuptools import setup, find_packages

setup(
    name='arifpaypython',
    version='0.1.2',
    author='Sina',
    author_email='b99174794@gmail.com',
    description='arifpay-python is a Python package that provides a simple interface for integrating with the ArifPay payment gateway.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'aiohttp'
    ], 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)