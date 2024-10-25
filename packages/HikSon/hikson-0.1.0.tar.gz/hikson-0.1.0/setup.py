from setuptools import setup, find_packages

setup(
    name="HikSon",  # This should be unique on PyPI
    version="0.1.0",
    author="Hikaro",
    author_email="contact@hikarox64.com",
    description="An easier method to read, edit, and save data in JSONs",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/1cz1/HikSon",  # Your GitHub repository or project link
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
