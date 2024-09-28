from importlib.metadata import entry_points
import pathlib
from setuptools import find_packages, setup

setup(
    name="brothers",
    version="0.0.1",
    description="Short description",
    package_dir={"": "brothers"},
    packages=find_packages(),
    include_package_data=True,
    long_description=pathlib.Path("README.md").read_text(), 
    long_description_content_type="text/markdown",
    url="https://github.com/poivronjaune/brothers",
    author="PoivronJaune",
    author_email="poivronjaune@gmail.com",
    license="MIT",
    project_urls={
        "Source" : "https://github.com/poivronjaune/brothers"
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Pytest",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    install_requires=[
        "pandas",
        "yfinance",
        "lightweight_charts"
    ],
    extras_require={
        "dev": ["pytest", "twine"],
    },
    python_requires=">=3.10",
    entry_points={"console_scripts": ["brothers = brothers.cli:main"]}
)
