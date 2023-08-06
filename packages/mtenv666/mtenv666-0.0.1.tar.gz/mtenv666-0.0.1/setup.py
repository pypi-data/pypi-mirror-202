
import codecs
import io
import os
import re
import sys
import webbrowser
import platform
import configparser
try:
    from setuptools import setup
except:
    from distutils.core import setup
"""
"""

with io.open('mtenv/__init__.py', 'rt', encoding='utf8') as f:
    context = f.read()
    VERSION = re.search(r'__version__ = \'(.*?)\'', context).group(1)
    AUTHOR = re.search(r'__author__ = \'(.*?)\'', context).group(1)


def read(fname):

    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "mtenv666"
"""
"""
PACKAGES = ["mtenv"]
"""
"""

DESCRIPTION = "环境参数"


"""
"""

KEYWORDS = [ "quant", "finance", ]
"""
"""

AUTHOR_EMAIL = "3491360008@qq.com"



LICENSE = "MIT"


# py -m build
# twine upload dist\*
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description='Mortisetenon Environment',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'mtenv_set = mtenv.__init__:set_data_account',
        ]
    },
    # install_requires=requirements,
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True
)