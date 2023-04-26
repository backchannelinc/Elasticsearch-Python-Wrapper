#!/usr/bin/env python

from distutils.core import setup
from espywrapper.__version__ import getVersion

setup(
      name='espywrapper',
      version=getVersion(),
      description='Python package for querying Elasticsearch databases, optimized for SQL querying and dataframe usage.',
      author='@backchannelre',
      author_email='developers@backchannel.re',
      url='https://github.com/backchannelinc/Elasticsearch-Python-Wrapper',
      install_requires=[
        'certifi',
        'requests',
        'urllib3',
        'pandas',
        'elasticsearch'
      ],
      packages=['espywrapper']
)
