#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

import os
import sys
import textwrap

extra_tests_require = []
if sys.version_info < (3, 0):
    extra_tests_require.append('mock==1.0.1')

ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
    name='django-bouncy',
    version='0.0.1',
    author='Nick Catalano',
    packages=['django_bouncy', 'django_bouncy.migrations', 'django_bouncy.tests',],
    url='https://github.com/ofa/django-bouncy',
    description="A way to handle bounce and abuse reports delivered by Amazon's Simple Notification Service regarding emails sent by Simple Email Service",
    long_description=textwrap.dedent(open(os.path.join(ROOT, 'README.rst')).read()),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.4',
        'python-dateutil>=2.1',
        'pyopenssl>=0.13.1',
        'pem>=0.1.0'
    ],
    tests_require=[
          'nose>=1.3',
          'django-setuptest>=0.1.4',
    ] + extra_tests_require,
    test_suite='setuptest.setuptest.SetupTestSuite',
    keywords = "aws ses sns seacucumber boto",
    classifiers=['Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Topic :: Internet :: WWW/HTTP']
)
