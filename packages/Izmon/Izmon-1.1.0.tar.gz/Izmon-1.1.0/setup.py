import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="Izmon",
    version="1.1.0",
    install_requires=[
        "requests",
    ],
    license="GPLv2",
    author="Yohei Akita, nabe, miso",
    author_email="akita.yohei0724@gmail.com",
    description="You can play Izmon with this libraly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akita0724",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
