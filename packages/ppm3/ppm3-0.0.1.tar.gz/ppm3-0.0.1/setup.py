from setuptools import setup, find_packages

setup(
    name="ppm3",
    version="0.0.1",
    packages=find_packages(),
    # package_dir={"": "ppm3"},
    install_requires=[
        "ansicon == 1.89.0",
        "blessed == 1.20.0",
        "editor == 1.6.6",
        "inquirer == 3.4.0",
        "jinxed == 1.3.0",
        "readchar == 4.2.0",
        "runs == 1.2.2",
        "setuptools == 75.2.0",
        "six == 1.16.0",
        "wcwidth == 0.2.13",
        "xmod == 1.8.1",
    ],
    entry_points={
        "console_scripts": [
            "ppm=ppm3:main",  # Pointing directly to main.py
        ],
    },
)
