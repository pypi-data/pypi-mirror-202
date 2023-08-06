from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "A function to facilitate the Ahead-of-time compilation with Numba"

# Setting up
setup(
    name="numba_aot_compiler",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/numba_aot_compiler',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    desc=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['deepcopyall', 'numba', 'ordered_set', 'touchtouch'],
    keywords=['numba', 'aot', 'compile'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['deepcopyall', 'numba', 'ordered_set', 'touchtouch'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*