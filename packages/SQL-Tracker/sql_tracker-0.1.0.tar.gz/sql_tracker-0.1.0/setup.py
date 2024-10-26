from setuptools import setup, find_packages

setup(
    name="SQL_Tracker",  # Unique on PyPI
    version="0.1.0",           # Follow Semantic Versioning
    description="Real-time SQL query tracking and lineage visualization.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sagar Sambhwani",
    author_email="sagar.2001.a20@gmail.com",
    url="https://github.com/sagarsambhwani/SQL_Tracker",
    packages=find_packages(),  # Automatically find packages in your directory
    install_requires=[
        "sqlparse>=0.4.4",
        "prettytable>=3.6.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
