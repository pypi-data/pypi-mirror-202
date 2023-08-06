from setuptools import setup, find_packages

with open("./src/gitstorage/__version__.py") as f:
    exec(f.read(), globals())

setup(
    name="gitstorage",
    version=globals()["__version__"],
    description="A library that uses git version control system to store and synchronize files",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    author="TheMasterOfMagic",
    author_email="",
    url="https://github.com/themasterofmagic/gitstorage",
    packages=find_packages("src"),
    install_requires=open("requirements.txt").read().strip().splitlines(),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
