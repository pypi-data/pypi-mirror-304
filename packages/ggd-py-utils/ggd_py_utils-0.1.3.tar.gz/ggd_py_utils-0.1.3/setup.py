from setuptools import setup, find_packages

setup(
    name="ggd-py-utils",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    description="A collection of utility functions for my projects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Gerardo Ignacio Galdames Díaz",
    author_email="gerardogaldames@gmail.com",
    url="https://github.com/ggaldamesd/ggd-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "faiss-cpu==1.8.0",
        "unidecode==1.3.8",
        "colorama==0.4.6",
        "chime==0.7.0",
        "fasttext-wheel==0.9.2",
        "plotly==5.22.0",
        "nltk==3.8.1",
        "tf_keras==2.18.0",
        "torch==2.2.2",
        "numpy==1.26.4",
        "sentence-transformers==3.0.1",
    ],
)
