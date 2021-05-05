import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signalploter-V2", # Replace with your own username
    version="0.0.1",
    author="Kwinten v. Meerbeek; Jowan Pittevils",
    author_email="jowan.pittevils@telenet.be",
    description="A package for exploring databases and plotting biomedical data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jowanpittevils/Databasemanager_Signalplotter",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD 3-Clause",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["matplotlib","PyQt5","numpy","datetime","pyqtgraph"],
    python_requires=">=3.6",
)