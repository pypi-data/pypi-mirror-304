from setuptools import setup, find_packages

setup(
    name="raintools_colors",
    version="0.1.1",
    description="A simple module to print colored text in the terminal",
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
