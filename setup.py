"""
Setup script for Cohort Validator package.
"""

import os

from setuptools import find_packages, setup


# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


# Read requirements from requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [
                line.strip() for line in f if line.strip() and not line.startswith("#")
            ]
    return []


setup(
    name="cohort-validator",
    version="1.0.0",
    author="EPAM Systems",
    author_email="cohort-validator@epam.com",
    description="Python interface to OHDSI CIRCE cohort validation library",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/OdyOSG/ohdsi-cohort-validator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "httpx>=0.25.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cohort-validate=cohort_validator.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cohort_validator": ["*.jar", "*.json"],
        "*": ["circe-be/**/*"],
    },
    zip_safe=False,
)
