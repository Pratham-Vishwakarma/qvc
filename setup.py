from setuptools import setup, find_packages

setup(
    name="qvc",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "qvc=qvc.cli:main",
        ],
    },
)