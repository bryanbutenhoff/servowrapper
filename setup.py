from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="servowrapper",
    version="0.0.1",
    packages=['servowrapper'],
    license='Apache 2.0',
    description="A wrapper package for dynamixel servo control",
    long_description=open('./README.md').read(),
    author="Bryan Butenhoff",
    author_email="bryanbutenhoff@vt.edu",
    url="https://github.com/bryanbutenhoff/servowrapper",
)
