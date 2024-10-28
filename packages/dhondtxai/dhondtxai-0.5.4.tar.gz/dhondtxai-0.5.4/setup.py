
from setuptools import setup, find_packages

setup(
    name='dhondtxai',
    version='0.5.4',
    author='Türker Berk DÖNMEZ',
    author_email='turkerberkdonmez@gmail.com',
    description="An explainability tool for machine learning models using the D'Hondt method.",
    url='https://github.com/turkerbdonmez/dhondtxai',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'scikit-learn',
        'catboost'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
