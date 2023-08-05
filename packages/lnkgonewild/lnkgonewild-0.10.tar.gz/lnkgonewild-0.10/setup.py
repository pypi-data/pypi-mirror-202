from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Creates .lnk files (with admin rights if desired), can execute any file in hidden mode (no more bothersome popups when executing .bat/.cmd files)"

# Setting up
setup(
    name="lnkgonewild",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/lnkgonewild',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['nutikacompile'],
    keywords=['hidden', 'subprocess', 'windows', 'lnk', 'links', 'shortcuts'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['nutikacompile'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*