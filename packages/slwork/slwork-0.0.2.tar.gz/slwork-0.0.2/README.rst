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

Run the command to install the slwork package

::

    python setup.py install

After successful installation, when using the mode_5.py
script of this package in other scripts, add a reference statement


::

   from slwork.mode_5 import *


When updating the package next time, you will need to:
1. Delete compressed files and folder
2. Run commands to uninstall packages in Python environment

::

    pip3 uninstall slwork


Then reinstall it again according to the installation method



