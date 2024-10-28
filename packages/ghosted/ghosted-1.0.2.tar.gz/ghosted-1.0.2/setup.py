from setuptools import setup, find_packages

setup(
    name="ghosted",
    version="1.0.2",
    description="A Python library for synthetic data generation, data blending, anomaly injection, and noise injection.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Andrea Wright Morgan",
    author_email="andreawright0813@gmail.com",
    url="https://github.com/awright813/ghosted",
    packages=find_packages(include=["ghosted", "ghosted.*"]),
    include_package_data=True,
    install_requires=[
        "copulas>=0.11.1",
        "matplotlib>=3.9.2",
        "numpy>=2.1.2",
        "pandas>=2.2.3",
        "pytest>=8.3.3",
        "scipy>=1.14.1",
        "seaborn>=0.13.2",
        "setuptools>=75.2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12"
)
