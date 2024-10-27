from setuptools import setup, find_packages

setup(
    name="roswagger",
    version="2.0",
    author="RoSwagger Developers",
    author_email="support@roswagger.com",
    description="A Python package for accessing RoSwagger API endpoints",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://roswagger.com",
    packages=find_packages(),
    install_requires=["requests", "python-dateutil"],  # Dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
