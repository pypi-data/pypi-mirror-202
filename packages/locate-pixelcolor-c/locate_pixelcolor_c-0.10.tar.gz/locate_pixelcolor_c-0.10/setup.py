from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Detects colors in images 10 x faster than Numpy "

# Setting up
setup(
    name="locate_pixelcolor_c",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/locate_pixelcolor_c',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['numpy'],
    keywords=['C', 'image', 'search', 'rgb'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['numpy'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*