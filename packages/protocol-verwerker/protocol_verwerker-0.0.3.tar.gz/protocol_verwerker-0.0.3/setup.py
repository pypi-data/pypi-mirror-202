import setuptools

setuptools.setup(
    name="protocol_verwerker",
    version="0.0.3",
    description = "Een python script om een sequentietabel te genereren uit een protocol.",
    readme = "README.md",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    dependencies = [
        "pandas"
    ],
    install_requires=["pandas"],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "protocol_verwerker = protocol_verwerker.__main__:main"
        ]
    }
)