from setuptools import setup, find_packages

# open license
with open("LICENSE") as f: license = f.read()

# setup
setup(
    name="openart",
    version="0.0.1",
    description="",
    author="Gabriel",
    author_email="041337@proton.me",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
    scripts=["openart/openart.py"]
)