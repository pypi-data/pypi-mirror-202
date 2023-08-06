from setuptools import setup, find_packages

classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

setup(
    name='capsolver-api',
    version='1.0.0',
    author='seadhy',
    author_email='seadhy@protonmail.com',
    description='capsolver python libary',
    long_description='i will write',
    long_description_content_type="text/markdown",
    url="https://github.com/seadhy/capsolver-py",
    project_urls={
        "Bug Tracker": "https://github.com/seadhy/capsolver-py/issues",
    },
    classifiers=classifiers,

    install_requires=[
        "requests",
    ],
    packages=find_packages(),
    package_dir={"capsolver_py": ""},
    include_package_data=True,
    python_requires=">=3.10.7",

)
