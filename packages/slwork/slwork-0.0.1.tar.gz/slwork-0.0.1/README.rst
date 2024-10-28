==============================
slwork Introduction
==============================



Introduction
==============================


Could be installed in the following two ways:

1. **Install using pip3**

- Install Python packages using pip

::

    pip3 install slowrk_function



- Use pip to update Python package commands

::

    pip3 install --upgrade slowrk_function


2. **Install using compressed file**

After decompressing the folder, enter the decompressed
file package and first enter the Python environment in
the command window

::

    conda activate vpy_slw

Run the command to install the slwork_function package

::

    python setup.py install

After successful installation, when using the mode_5.py
script of this package in other scripts, add a reference statement


::

   from slwork_function.mode_5 import *


