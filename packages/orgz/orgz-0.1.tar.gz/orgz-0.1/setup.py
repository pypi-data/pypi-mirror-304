from setuptools import setup, find_packages

setup(
    name="orgz",  # Your package name
    version="0.1",
    author="DanielClover",
    author_email="danielcaiyongjie@gmail.com",
    description="This is a widget designed for openGauss Database inspection Tool!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Dannyrevenger/orgz.git",  # Your project URL, if available
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "orgz=orgz.orgz:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)
