from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="i3pystatuscontrib.elisaroaming",
    version="0.1.2",
    author="Mikkula",
    author_email="pypi@mikkula1.org",
    description="Elisa roaming quota module for i3pystatus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mikkula/i3pystatuscontrib-elisaroaming",
    python_requires=">=3.6",
    packages=find_namespace_packages(include=["i3pystatuscontrib.*"]),
    zip_safe=False,
    install_requires=["requests"]
)
