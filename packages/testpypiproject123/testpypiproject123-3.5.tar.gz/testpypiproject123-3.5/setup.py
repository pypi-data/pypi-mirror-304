from setuptools import setup, find_packages

print("installed")

setup(
    name="testpypiproject123",
    version="3.5",
    author="super man",
    author_email="your.email@example.com",
    description="package that helps prevent malicious user from abusing unused package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your_project",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
