# Author: Supper-Smille <ak2004@support.email.ne.jp>
# Copyright (c) 2023 Supper-Smille
# License: MIT License


from setuptools import setup
import MyJpHolidays
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    

DESCRIPTION = "MyJpHolidays: You get a combined list of Japan-Holidays. You can customize orignal holidays used ini-file."
NAME = 'MyJpHolidays'
AUTHOR = 'Supper-Smille'
AUTHOR_EMAIL = 'ak2004@support.email.ne.jp'
URL = 'https://github.com/Supper-Smille/MyJpHolidays20230412'
LICENSE = 'MIT License'
DOWNLOAD_URL = 'https://github.com/Supper-Smille/MyJpHolidays20230412'
VERSION = MyJpHolidays.__version__
PYTHON_REQUIRES = ">=3.8.10"


INSTALL_REQUIRES = [
    'numpy >=1.23.1'
]


PACKAGES = [
    'MyJpHolidays'
]


CLASSIFIERS = [
		'Development Status :: 4 - Beta',
		#'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Environment :: Win32 (MS Windows)',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        #'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Software Development :: Libraries'
]

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      
      # extras_require=EXTRAS_REQUIRE,
      
      packages=PACKAGES,
      classifiers=CLASSIFIERS
    )

