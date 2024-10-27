from setuptools import setup
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='zico',
    version='1.0.1',
    description='tes zico',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='okyx',
    author_email='zicolazicola@gmail.com',
    packages=setuptools.find_packages(),
    license='MIT'
)