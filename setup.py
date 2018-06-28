"""
    Copyright (C) 2018 Matthew LeMieux
    
    This file is part of a third party TDAmeritrade API Library, called MLTDAmeritrade.

    MLTDAmeritrade is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MLTDAmeritrade is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MLTDAmeritrade.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup
import setuptools

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements


reqs = parse_requirements('./requirements.txt', session=False)
install_requires = [str(ir.req) for ir in reqs]

setup(name='tdameritrade',
      version='0.1.1',
      description='Matthew''s TD Ameritrade API Python Library',
      url='',
      author='Matthew LeMieux',
      author_email='mdl@mlemieux.com',
      license='GPLv2',
      packages=setuptools.find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      zip_safe=False)
