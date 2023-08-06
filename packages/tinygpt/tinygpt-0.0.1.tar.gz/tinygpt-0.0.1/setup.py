from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A tiny GPT for educational purpose"
LONG_DESCRIPTION = "A tiny GPT for educational purpose"

setup(
    name="tinygpt",
    version=VERSION,
    author="Quan Hua",
    author_email="<quanhua92@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "first package"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
    ],
)
