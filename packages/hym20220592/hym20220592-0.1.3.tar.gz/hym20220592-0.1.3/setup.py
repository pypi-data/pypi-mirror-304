from setuptools import setup, find_packages

setup(
    name='hym20220592',
    version='v0.1.3',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'openpyxl',
        'numpy',
        'matplotlib',
        'pandas'
    ],
)
