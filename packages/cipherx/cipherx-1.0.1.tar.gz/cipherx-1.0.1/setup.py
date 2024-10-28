from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cipherx",  # Ensure this name is unique on PyPI
    version="1.0.1",
    author="Christian Johnson",
    author_email="cjohnson@metisos.com",
    description="A custom SPN cipher implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where='.'),  # Search for packages from the root directory
    include_package_data=True,  # Include non-code files like README.md
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'cipherx=cipher.cli:main',  # Entry point for the CLI tool
        ],
    },
)
