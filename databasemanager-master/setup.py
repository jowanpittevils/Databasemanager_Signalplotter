import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="databasemanager", # Replace with your own username
    version="0.0.1",
    author="Amir H. Ansari",
    author_email="amirans65.ai@gmail.com",
    description="A package for organizing databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/amirans65/databasemanager",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: BSD 3-Clause",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.6',
    install_requires=['mne','prettytable','tqdm', 'scipy','numpy','psutil'],
)