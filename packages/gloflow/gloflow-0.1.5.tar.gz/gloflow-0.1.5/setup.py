from setuptools import setup, find_packages

setup(
    name="gloflow",
    version="0.1.5",
    author="Ivan Trajkovic",
    author_email="glofloworg@gmail.com",
    description="""
Py package for interacting with the gloflow platform API's.
""",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gloflow/gloflow",
    packages=find_packages(
        where="src",
        exclude=[
            "src/deprecated"
        ]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",  # Example dependency
    ],
    package_dir={"": "src"},  # Base directory for packages is src/
)
