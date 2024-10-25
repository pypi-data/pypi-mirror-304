import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aimmo_woody", # Replace with your own username
    version="0.0.1",
    author="woody",
    author_email="woosolhwi@gmail.com",
    description="functions that i use frequently in aimmo.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woosolhwi",
    project_urls={
        "Bug Tracker": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)