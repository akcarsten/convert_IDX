import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="convert_IDX",
    version="0.0.1",
    url="https://github.com/akcarsten/convert_IDX",
    author="Carsten Klein",
    description="Read and write IDX image datasets e.g. MNIST",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

