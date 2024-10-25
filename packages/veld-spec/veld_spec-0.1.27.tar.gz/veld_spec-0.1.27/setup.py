from setuptools import setup, find_packages

setup(
    name="veld_spec",
    version="0.1.27",
    packages=["veld_spec_f"],
    author="Stefan Resch",
    author_email="stefan.resch@oeaw.ac.at",
    description="VELD specification",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/acdh-oeaw/VELD_spec",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "PyYAML>=6.0.2",
    ],
    include_package_data=True,
    package_data={"veld_spec_f": ["README.md"]},
)

