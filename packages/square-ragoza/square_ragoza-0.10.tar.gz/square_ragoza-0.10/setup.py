from setuptools import setup, find_packages
import codecs
import os
#Project library (Rauf Gozal 214076IVSB)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = 'Function'
LONG_DESCRIPTION = 'Simple function'

# Setting up
setup(
    name="square_ragoza",
    version=VERSION,
    author="Rauf Gozal",
    author_email="<raufgozel@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python', 'square'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)