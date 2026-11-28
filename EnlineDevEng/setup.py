from setuptools import find_packages, setup

pacotes_src = find_packages(where="src")

setup(
    packages=pacotes_src + ["EnlineDevEng.output", "EnlineDevEng.tests"],
    package_dir={
        "": "src",
        "EnlineDevEng.output": "output",
        "EnlineDevEng.tests": "tests",
    },
)