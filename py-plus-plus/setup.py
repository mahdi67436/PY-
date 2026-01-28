"""Setup script for py++ distribution."""

import os
from setuptools import setup, find_packages

# Read README if it exists
def read_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='pypp-lang',
    version='0.2.0',
    author='py++ Team',
    author_email='team@pypp.dev',
    description='py++: Python-like language with C++ speed, advanced data structures, and professional tooling',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/py-plus-plus',
    project_urls={
        'Documentation': 'https://github.com/yourusername/py-plus-plus/docs',
        'Source': 'https://github.com/yourusername/py-plus-plus',
        'Tracker': 'https://github.com/yourusername/py-plus-plus/issues',
    },
    packages=find_packages(),
    package_data={
        'src': ['*.py'],
    },
    entry_points={
        'console_scripts': [
            'pypp=pypp_cli:main',
        ],
    },
    python_requires='>=3.7',
    install_requires=[
        # No external dependencies - pure Python implementation
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.10',
        ],
    },
    keywords=[
        'language', 'interpreter', 'programming', 'compiler', 'python',
        'arrays', 'objects', 'sets', 'advanced', 'features'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Compilers',
    ],
    zip_safe=False,
)
