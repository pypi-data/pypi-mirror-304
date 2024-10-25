import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="synthguard",
    version="0.0.1",
    author="ktamm",
    author_email="kristian.tamm@cyber.ee",
    description="Syhtesized data generation pipeline module library",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/kristiantamm/synthguard",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='synthetic data, privacy, machine learning',
)
