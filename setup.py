#!/usr/bin/env python

from setuptools import setup
import textwrap

setup(
    name='django-bouncy',
    version='0.0.1',
    author='Nick Catalano',
    packages=['django_bouncy',],
    url='https://github.com/ofa/django-bouncy',
    description="A way to handle bounce and abuse reports delivered by Amazon's Simple Notification Service regarding emails sent by Simple Email Service",
    long_description=textwrap.dedent(open('README.rst', 'r').read()),
    install_requires=[
        'Django>=1.5',
        'South>=0.8.1',
        'python-dateutil>=2.1',
        'pyopenssl>=0.13.1',
        'pem>=0.1.0'
    ],
    tests_require=[
          'mock>=1.0.1'
    ],
    keywords = "aws ses sns seacucumber boto",
    classifiers=['Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Topic :: Internet :: WWW/HTTP'],
    use_2to3=True,
)
