# PyLeon

[![License](http://img.shields.io/:license-affero-blue.svg)](http://www.gnu.org/licenses/agpl-3.0.en.html)

# What is PyLeon?

PyLeon is a Python wrapper around the .fasta/.fastq compression suite Leon (https://github.com/GATB/Leon).

# Setup

## Requirements

CMake 3.1+; see http://www.cmake.org/cmake/resources/software.html

c++/11 compiler; compilation was tested with gcc and g++ version>=4.8 (Linux) and clang version>=3.6 (Mac OSX).

## Instructions

    # get a local copy of source code
    git clone --recursive https://github.com/jdvne/pyleon

    # compile Leon code and add pyleon to your user's python modules
    sh INSTALL

    # ensure Leon has build properly
    python3 test.py