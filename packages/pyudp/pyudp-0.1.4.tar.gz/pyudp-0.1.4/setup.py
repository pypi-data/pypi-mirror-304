from setuptools import find_packages, setup

setup(
    name="pyudp",
    version="0.1.4",
    description="A simple wrapper for UDP communication in Python, with multicast support.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="takumi-nishimura",
    author_email="clp13218@nitech.jp",
    url="https://github.com/takumi-nishimura/PyUDP",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
