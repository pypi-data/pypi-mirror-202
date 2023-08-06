"""The python wrapper for IQ Option API package setup."""
from setuptools import setup, find_packages
#from myiqoptionapi.iqoptionapi.version_control import api_version

setup(
    name="my-iqoptionapi",
    version="7.1.1",
    packages=find_packages(),
    install_requires=["pylint", "requests", "websocket-client==0.56"],
    include_package_data=True,
    description="Best IQ Option API for python",
    long_description="Best IQ Option API for python",
    url="https://github.com/zskull-py/iqoptionapi",
    author="zSkull.py",
    keywords="iqoption",
    zip_safe=False
)
