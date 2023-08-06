from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lantools-nsa",
    version="0.0.2",
    description="",
    py_modules=["arabic_parser"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Alaa' Omar",
    author_email="",

    install_requires = [
    'six==1.16.0',
    'farasapy==0.0.14',
    'tqdm==4.62.2',
    'requests==2.25.1',
    'regex==2021.4.4'
    ],

    extras_require = {
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine",
        ],
    },
)
