from setuptools import setup, find_packages

setup(
    name="bgc_cloud",  # Name of your package
    version="0.1.0",  # Version of your package
    description="BGC cloud helper",
    author="Abuti Martin",
    author_email="your.email@example.com",
    url="https://github.com/Enrique-Mertoe/bgc_cloud",  # Project URL
    packages=find_packages(),  # Automatically finds packages
    install_requires=[  # List of dependencies
        "requests"
    ],
    classifiers=[  # Optional: Package classification
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Python version requirement
)
