#!/usr/bin/env python
#
# Copyright 2013 Alan Quillin
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

version = '0.0'

setup(name='myhvac_web',
      version=version,
      description='',
      long_description='',
      keywords='',
      author='Alan Quillin',
      author_email='alanquillin@gmail.com',
      url='https://github.com/alanquillin/myhvac_web',
      license='Apache Software License',
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'License :: OSI Approved :: Apache Software License',
                   'Framework :: Flask',
                   'Topic :: Home Automation'],
      include_package_data=True,
      zip_safe=False,
      install_requires=reqs
      )