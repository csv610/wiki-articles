"""Setup configuration for WikiArticles package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()]

setup(
    name="wikiartcles",
    version="1.0.0",
    author="CSV610",
    description="A Python tool to fetch Wikipedia articles in multiple languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wikiartcles",
    py_modules=["search_wiki_article"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    include_package_data=True,
)
