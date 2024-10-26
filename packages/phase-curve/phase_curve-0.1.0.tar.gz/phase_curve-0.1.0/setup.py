import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phase_curve",
    version="0.1.0",
    author="Pedro Bernardinelli",
    author_email="phbern@uw.edu",
    description=" Lightweight, bare bones asteroid phase curve fitter ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bernardinelli/phase_curve",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    packages=["phase_curve"],
    python_requires=">=3.6",
    install_requires=["numpy", "scipy"],
)
