#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['requests',
                'numpy',
                'pandas',
                'matplotlib',
                'astropy']

test_requirements = ['pytest>=3']

setup(
    author="Wang Weihua",
    author_email='wangwh@czu.cn',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Legacyplate Data Query",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='legacyplatequery',
    name='legacyplatequery',
    packages=find_packages(include=['legacyplatequery', 'legacyplatequery.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/wangweihua/legacyplatequery',
    version='0.1.1',
    zip_safe=False,
)
