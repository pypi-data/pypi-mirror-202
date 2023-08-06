from setuptools import find_packages, setup
setup (
    name = 'DataStructuresLiamTheodore',
    packages=find_packages(include=['datastructures.linear', 'datastructures.nodes', 'datastructures.trees']),
    version='1.0.4',
    description='Datastructures library for ENSF 338 Final Project.',
    author='Theodore and Liam',
    author_email='liam.mah@ucalgary.ca',
)