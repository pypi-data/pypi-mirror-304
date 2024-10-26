from setuptools import setup, find_packages

setup(
    name='trino_connector',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},  
    install_requires=[
        'trino>=0.318.0',
        'pandas>=1.0.0',
        'urllib3>=1.26.0',
    ],
    description='A simple Trino connector library',
    url='https://github.com/Carrillo26/trino_connector',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
