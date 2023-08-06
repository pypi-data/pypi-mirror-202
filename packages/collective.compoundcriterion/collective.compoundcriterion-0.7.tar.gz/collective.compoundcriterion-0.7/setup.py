# -*- coding: utf-8 -*-
"""Installer for the collective.compoundcriterion package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read() + '\n' +
    'Contributors\n============\n' + '\n' + open('CONTRIBUTORS.rst').read() +
    '\n' + open('CHANGES.rst').read() + '\n')

setup(
    name='collective.compoundcriterion',
    version='0.7',
    description="Compound criterion for plone.app.collection managing complex query",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Plone collection criterion',
    author='IMIO',
    author_email='support@imio.be',
    url='http://pypi.python.org/pypi/collective.compoundcriterion',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'imio.helpers',
        'plone.api',
        'setuptools',
        'archetypes.querywidget >= 1.1.2',
    ],
    extras_require={
        'test': [
            'ftw.labels',
            'plone.app.testing',
            'plone.app.robotframework',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
