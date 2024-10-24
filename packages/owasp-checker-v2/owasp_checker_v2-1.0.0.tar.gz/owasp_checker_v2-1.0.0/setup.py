#!/usr/bin/env python3
"""
Setup configuration for OWASP Checker V2.
"""

from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='owasp-checker-v2',
    version='1.0.0',
    description='Enhanced OWASP Top Ten Compliance Checker Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='ABidi Bassem',
    author_email='abidi.bassem@me.com',
    url='https://github.com/abidi-bassem/owasp-checker-v2',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.0.0',
            'black>=21.0.0',
            'isort>=5.0.0',
            'mypy>=0.900',
            'flake8>=3.9.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'owasp-checker=owasp_checker_v2.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
    python_requires='>=3.8',
    keywords='security, owasp, vulnerability, scanner, dependency-checker, threat-intelligence',
    project_urls={
        'Documentation': 'https://github.com/abidi-bassem/owasp-checker-v2/docs',
        'Source': 'https://github.com/abidi-bassem/owasp-checker-v2',
        'Tracker': 'https://github.com/abidi-bassem/owasp-checker-v2/issues',
    },
)
