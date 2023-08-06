from setuptools import setup, find_packages

setup(
    name='arsalan-khaleel-338package',
    version='0.1',
    author= 'arsalan_khaleel',
    author_email='arsalan.khaleel@ucalgary.ca',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'scipy'
    ],
)
