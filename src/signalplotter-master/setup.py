import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signalplotter", 
    version="0.0.1",
    author="Amir H. Ansari",
    author_email="amirans65.ai@gmail.com",
    description="This toolbox is for easily plotting multichannel timeseries like EEG, ECG, speech, etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "LicenseM :: OSI Approved :: IT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.6',
    install_requires=['numpy', 'matplotlib', 'pyqt5', 'pyqtgraph'],
)
