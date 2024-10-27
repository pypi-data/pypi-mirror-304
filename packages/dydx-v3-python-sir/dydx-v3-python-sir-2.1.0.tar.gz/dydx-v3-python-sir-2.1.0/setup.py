from setuptools import setup, find_packages

LONG_DESCRIPTION = open('README.md', 'r').read()

REQUIREMENTS = [
    'aiohttp>=3.8.1',
    'cytoolz>=0.12.1',
    'dateparser>=1.0.0',
    'ecdsa>=0.18.0',
    'eth_keys',
    'eth-account>=0.9.0',
    'mpmath>=1.3.0',
    'requests>=2.31.0',
    'six>=1.16.0',
    'sympy>=1.13.2',
    'web3>=6.5.0',
]

setup(
    name='dydx-v3-python-sir',
    version='2.1.0',
    packages=find_packages(),
    package_data={
        'dydx3': [
            'abi/*.json',
            'starkex/starkex_resources/*.json',
        ],
    },
    description='dYdX Python REST API for Limit Orders - sir_even fork',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/sirEven/dydx-v3-python',
    author='dYdX Trading Inc. - sirEven fork',
    license='Apache 2.0',
    author_email='sir_even@icloud.com',
    install_requires=REQUIREMENTS,
    keywords='dydx exchange rest api defi ethereum eth',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',  # General version, include only '3'
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',  # Removed specific patch version
        'Programming Language :: Python :: 3.11',  # Removed specific patch version
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
