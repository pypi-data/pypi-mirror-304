from setuptools import setup, find_packages

setup(
    name="check-health",
    version="0.1.0",
    author="Fateme Samandarnejad",
    author_email="fsamandarnejad2001@gmail.com",
    description="A Python package for monitoring health checks of programs.",
    packages=find_packages(),
    install_requires=[
        "psutil>=6.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
