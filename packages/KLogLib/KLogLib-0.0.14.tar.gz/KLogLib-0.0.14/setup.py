import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
PACKAGE_NAME =  'KLogLib'
AUTHOR = 'Javier Frias Jimenez'
AUTHOR_EMAIL = 'javifriasj@gmail.com'
URL = 'https://github.com/javifriasj/KLog/releases/tag/0.0.4'
LICENSE = 'MIT license'
DESCRIPTION = 'Simple Log library'
LONG_DESCRIPTION = open('README.md').read()
LONG_DESC_TYPE = "text/markdown"
INSTALL_REQUIRES = [

]

setup(name = PACKAGE_NAME,
      Description=DESCRIPTION,
      Long_description=LONG_DESCRIPTION,
      Long_description_content_type=LONG_DESC_TYPE,
      Author=AUTHOR,
      License=LICENSE,
      Author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
)