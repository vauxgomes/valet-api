#!/usr/bin/env python3

# Author: Vaux Gomes
# Contact: vauxgomes@gmail.com
# Version: 1.0

from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'Valet API Service'
LONG_DESCRIPTION = 'Valet Network Anomaly Detection API Service'

setup(
    name="valet",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Vaux Gomes, Eduarda Valentim",
    author_email="vauxgomes@gmail.com, eduardacvalentim@gmail.com",
    packages=find_packages(),
    install_requires=['flask'],
    keywords=['anomaly detection', 'api']
)

'''
Setup Reference
- https://cibersistemas.pt/tecnologia/como-construir-seu-primeiro-pacote-python/
'''