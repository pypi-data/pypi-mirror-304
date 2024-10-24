from setuptools import setup, find_packages
import subprocess
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="trywebscraping",
    version="0.1.37",
    author="Luke Lucas",
    author_email="luke.lucas@trywebscraping.com",
    description="A fast web scraping library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/trywebscraping",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml",
        "selenium",
        "webdriver_manager",
        "click",
        "cryptography",
        "curl_cffi",
        "twine",
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'black',
            'isort',
        ],
    },
    entry_points={
        "console_scripts": [
            "trywebscraping=trywebscraping.cli:main",
            "trywebscraping-setup=trywebscraping.setup_script:main",
        ],
    },
    package_data={
        "trywebscraping": ["py.typed"],
    },
)