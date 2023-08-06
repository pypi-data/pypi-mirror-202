import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modelcdb", # Replace with your own username
    packages=['modelcdb'],
    version="0.1",
    author="WoojinCho",
    author_email="wooju_1@iae.re.kr",
    description="AI Model Store & Load through Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IAEWoojinCho",
    #packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
