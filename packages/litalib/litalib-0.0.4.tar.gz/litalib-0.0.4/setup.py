from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'A package of ALMS lighting data process'
LONG_DESCRIPTION = 'A set of python tools for processing ALMS lighting data'

setup(
    name="litalib",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Zhenyu Wang",
    author_email="wonstran@hotmail.com",
    license='MIT',
    packages=find_packages(),
    keywords='litalib',
    url = 'https://its.cutr.usf.edu/alms/',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    install_requires = [
        'numpy',
        'pandas',
        'matplotlib',
        'geopandas'
    ],
    python_requires='>=3.7'
)