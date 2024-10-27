from setuptools import find_packages
from setuptools import setup

setup(
    name='mantrapy',
    version='0.0.2',
    description='A Python lib to interact with the Mantra chain',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Quantum-Architects/mantrapy',
    author='Quantum-Architects',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'base58>=2.1.1',
        'bech32>=1.2.0',
        'ecdsa>=0.19.0',
        'fastapi>=0.115.3',
        'googleapis-common-protos>=1.61.0',
        'hdwallet>=2.2.1',
        'httpx>=0.27.2',
        'mnemonic>=0.21',
        'pydantic>=2.9.2',
        'pydantic-settings==2.6.0',
        'requests>=2.32.3',
        'SQLAlchemy>=2.0.36',
        'tenacity>=9.0.0',
        'uvicorn>=0.32.0',
        'websockets>=13.1',
    ],
)
