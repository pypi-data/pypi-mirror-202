import setuptools

with open("README.md", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="grammarette",
    use_scm_version={
        "write_to": "grammarette/_version.py",
        "write_to_template": '__version__ = "{version}"',
        "fallback_version": "???",
    },
    author="Jon Carr",
    author_email="jon.carr@rhul.ac.uk",
    description="A lightweight grammar inducer for toy lexicons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jwcarr/grammarette",
    license="GPLv3",
    packages=["grammarette"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.8",
    install_requires=["numpy>=1.20", "scipy>=1.5"],
    setup_requires=["setuptools_scm"],
)
