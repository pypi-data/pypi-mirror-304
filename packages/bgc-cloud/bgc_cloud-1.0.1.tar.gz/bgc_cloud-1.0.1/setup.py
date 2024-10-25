from setuptools import setup, find_packages

setup(
    name="bgc_cloud",
    version="1.0.1",
    description="BGC cloud helper",
    author="Abuti Martin",
    author_email="abutimartin778@gmail.com",
    url="https://github.com/Enrique-Mertoe/bgc_cloud",
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

# pypi-AgEIcHlwaS5vcmcCJDk1MWM3YjRiLTQ5MTUtNDBhNC04ODIxLTYxODJmMzRhZDUxYgACKlszLCIzYWEyZTQwYy00MjhlLTQ3MzMtYmFjOC03MWM5ODEwNDUxMmEiXQAABiBXyZ027KNdS27nEHKGHh-1A_L8QxpdZmaRQYWU2wwFzA