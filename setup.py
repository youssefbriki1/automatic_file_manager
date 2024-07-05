from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="automatic_file_manager", 
    version="0.0.1",
    author="Youssef Briki",
    author_email="youssef.briki05@gmail.com",
    description="Automatic file manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/youssefbriki1/automatic_file_manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
