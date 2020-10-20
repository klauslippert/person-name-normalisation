import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="personnamenorm", 
    version="0.0.1",
    author="Klaus Lippert",
    author_email="lippert@zbmed.de",
    description="unifying person names in different notations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/klauslippert/person-name-normalisation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic"
    ],
    install_requires=[
        "nltk >= 3.5",
        "ftfy >= 5.8"
    ]
)
