#!/usr/bin/env python3

import os
import setuptools


def _read_reqs(relpath):
    fullpath = os.path.join(os.path.dirname(__file__), relpath)
    with open(fullpath) as f:
        return [s.strip() for s in f.readlines()
                if (s.strip() and not s.startswith("#"))]


_REQUIREMENTS_TXT = _read_reqs("requirements.txt")


setuptools.setup(
    name='blip-vit-fork',
    version='0.0.3',
    install_requires=_REQUIREMENTS_TXT,
    include_package_data=True,
    package_data={'': [
        '*.txt',
        '*.yaml',
        '*.json'
    ]},
    classifiers=[],
    description='BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation',
    author='salesforce',
    author_email='junnan.li@salesforce.com',
    url='https://github.com/nateagr/BLIP',
    packages=setuptools.find_packages()
)
