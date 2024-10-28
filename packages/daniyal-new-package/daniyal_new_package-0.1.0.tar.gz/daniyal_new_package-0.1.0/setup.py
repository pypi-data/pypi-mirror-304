from setuptools import setup, find_packages

setup(
    name="daniyal_new_package",
    version="0.1.0",
    description="This is the description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Daniyal Saif",
    author_email="daniyalsaif200@gmail.com",
    url="https://github.com/daniyalsaif/my_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)