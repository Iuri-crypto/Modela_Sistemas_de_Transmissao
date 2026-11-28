from setuptools import find_packages, setup

pacotes_src = find_packages(where="src")

setup(
    packages=pacotes_src + ["EnlineDevEng.tests"],
    package_dir={
        "": "src",
        "EnlineDevEng.tests": "tests",
    },
)