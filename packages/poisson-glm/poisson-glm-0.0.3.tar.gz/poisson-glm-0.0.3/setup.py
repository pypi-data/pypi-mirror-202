from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'Poisson GLM package for investigating spike trains in RGCs population. The model can use either radial basis function or raised cosine bumps, since both were built for comparisons.'

# Setting up
setup(
    name="poisson-glm",
    version=VERSION,
    author="Meina Lin Wei",
    author_email="meina.lw12@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib', 'scipy', 'os'],
    keywords=['python', 'poissonGLM'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)