from setuptools import setup, find_packages

setup(
    name="random-greetings",
    version="0.1.0",
    description="A simple random greeting generator",
    author="Abdullah Mobeen",
    author_email="a.mobeenn@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
)