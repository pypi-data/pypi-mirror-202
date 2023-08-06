from setuptools import setup, find_packages

# open license
with open("LICENSE", "r", encoding="utf-8") as f: license = f.read()

# open readme
with open("README.md", "r", encoding="utf-8") as fh: long_description = fh.read()


# setup
setup(
    name="openart",
    version="0.0.2",
    description="",
    url="https://github.com/41337/openart",
    author="Gabriel",
    author_email="041337@proton.me",
    license=license,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "docs")),
    scripts=["openart/openart.py"]
)