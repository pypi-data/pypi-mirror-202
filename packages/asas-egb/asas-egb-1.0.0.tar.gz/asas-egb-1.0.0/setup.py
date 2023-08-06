import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asas-egb",
    version="1.0.0",
    author="Lili Dong",
    author_email="ncjllld@hit.edu.cn",
    description="A library for estimating allele-specific alternative splicing events using transcriptome data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncjllld/asas-egb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'asas-egb = asas_egb.run:main'],
    },
)
