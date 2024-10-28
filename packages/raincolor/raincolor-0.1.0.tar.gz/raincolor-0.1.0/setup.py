from setuptools import setup, find_packages

setup(
    name="raincolor",
    version="0.1.0",
    description="A versatile Python module for terminal color and style formatting, allowing easy customization of text appearance in command line applications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Plingenn",
    author_email="raintool@engineer.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    python_requires=">=3.6",
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)
