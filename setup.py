import re

import setuptools, os


def open_local(paths, mode="r", encoding="utf8"):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), *paths)
    return open(path, mode=mode, encoding=encoding)


with open_local(["cloudrecon", "__init__.py"]) as f:
    version = re.search(r"__version__ = [\"'](\d+\.\d+\.\d+)[\"']", f.read()).group(1)

with open_local(["README.md"]) as f:
    long_description = f.read()

install_requires = ["mergedeep>=1.1", "requests>=2.23", "pymongo>=3.10", "pyyaml>=5.3"]

setuptools.setup(
    name="cloudrecon",
    version=version,
    author="Nathaniel 'Q' Quist",
    author_email="qcuequeue@gmail.com",
    description="Cloud bucket/blob finder.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/3of3/cloudrecon",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=install_requires,
    entry_points={"console_scripts": ["cloudrecon=cloudrecon.cloudrecon:cli"]},
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
