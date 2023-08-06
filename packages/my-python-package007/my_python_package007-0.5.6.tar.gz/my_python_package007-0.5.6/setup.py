from setuptools import setup, find_packages

setup(
    name='my_python_package007',
    version='0.5.6',
    description='My awesome Python package v2',
    author='DipakMehta',
    author_email='dipak@zvolv.com',
    url='https://github.com/DipakMehta/python',
    long_description='we are trying new version',
    packages=find_packages(),
    # entry_points={ 'console_scripts': [ 'my_python_package007=my_python_package:test_hello_world' ] }
    install_requires=[
        'numpy',
        'pandas',# list of dependencies
    ],
)
