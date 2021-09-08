from setuptools import find_packages, setup

setup(
    name="readtft",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(include="src"),
    install_requires=[
        "matplotlib",
        "numpy",
        "opencv-python",
        "Pillow",
        "pytesseract",
    ],
)
