import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="poisson_glm_diss",
    version="1.0.0",
    author="Cameron Kent",
    author_email="cameron.kent@hotmail.co.uk",
    description="A small package for Poisson GLM functionality",
    long_description=long_description,
    include_package_data = True,
    long_description_content_type="text/markdown",
    url="https://github.com/cameronkent1",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
