#!/usr/bin/env python

from setuptools import setup

import os
# import sys
import textwrap

ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
    name='django-bouncy',
    version='0.2.7',
    author='Nick Catalano',
    packages=[
        'django_bouncy', 'django_bouncy.migrations', 'django_bouncy.tests'],
    url='https://github.com/ofa/django-bouncy',
    description=(
        "A way to handle bounce and abuse reports delivered by Amazon's Simple"
        " Notification Service regarding emails sent by Simple Email Service"
    ),
    long_description=textwrap.dedent(
        open(os.path.join(ROOT, 'README.rst')).read()),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.11',
        'python-dateutil>=2.1',
        'pyopenssl>=0.13.1',
        'pem>=16.0.0',
    ],
    keywords="aws ses sns seacucumber boto",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP']
)
