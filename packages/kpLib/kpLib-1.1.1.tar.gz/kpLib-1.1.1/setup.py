import glob
from pathlib import Path

from setuptools import find_packages, setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "kpLib.lib", # The first arguement is the name used in at the import statement.
        ["python/kpLib/interface.cpp"] + sorted(glob.glob("./src/*.cpp")),
        include_dirs=[
            "./src/",
        ],

        #To debug, uncomment these lines to build share library with debug info.
        #extra_compile_args=['-std=c++11', '-Wall', '-Werror', '-fPIC', '-O0', '-g'],
        #extra_link_args=['-g']
    )
]

tests_requires = ["pytest", "pymatgen"]
cli_requires = ["pymatgen", "click"]

with open(Path(__file__).parent.joinpath("README.md").resolve()) as f:
    long_description = f.read()

setup(
    name="kpLib", # The name appear in PyPI. Not necessarily the one used in import statement.
    version="1.1.1",
    #use_scm_version={
    #   'version_scheme': 'post-release'
    #},
    author="Yunzhe Wang",
    author_email="ywang393@jhu.edu",
    url="https://gitlab.com/muellergroup/kplib",
    description="Library for generating highly-efficient generalized Monkhorst-Pack K-point grids" \
                " to accelerate electronic structure calculations, like DFT.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages("python"),
    package_dir={"": "python"}, # Mark "./python" as the root this package.
    ext_modules=ext_modules, # Create a external module for this package.
    install_requires = [
        "pybind11",
        "spglib",
    ],
    setup_requires = [
        "pybind11",
        #"setuptools_scm"
    ],
    tests_require = tests_requires,
    extras_require = {
        'tests' : tests_requires,
        'cli' : cli_requires,
    },
    #python_requires=">=3.7",
    #cmdclass={"build_ext": build_ext},
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "kpgen = kpLib.cli:generate [cmd]",
        ],
    },
    keywords = [
        "Computational Materials Science",
        "Materials Simulation",
        "Electronic Structure",
        "K-points",
        "kpoint",
        "Density Functional Theory",
        "DFT",
        "VASP",
        "Crystal",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="Apache-2.0",
)
