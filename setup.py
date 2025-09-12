from setuptools import setup, find_packages

setup(
    name="ml_pipeline",
    version="0.1.0",
    description="Pipeline de machine learning con sklearn usando Titanic",
    author="Francisco Castillo",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "scikit-learn",
    ],
    python_requires=">=3.8",
)
