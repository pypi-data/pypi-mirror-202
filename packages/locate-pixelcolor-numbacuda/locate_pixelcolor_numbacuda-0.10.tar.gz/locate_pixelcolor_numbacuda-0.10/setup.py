from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "RGB search with numba.cuda - 10 x faster than numpy"

# Setting up
setup(
    name="locate_pixelcolor_numbacuda",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/locate_pixelcolor_numbacuda',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    desc=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['numba', 'numpy'],
    keywords=['numpy', 'numba', 'CUDA', 'rgb', 'search'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['numba', 'numpy'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*