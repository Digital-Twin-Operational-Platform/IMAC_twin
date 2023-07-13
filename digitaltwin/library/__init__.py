"""
This folder should contain all the main functions used by the computations. The organisation of this folder is up for stylistic debate.
Option 1:
    Create a single .py file for each related calculations/modules. Within this file will contain many functions and possibly some common variables
    that are used acrossed many functions.
Option 2:
    Each module is organised as a folder where there are multiple .py files to load. This subfolder will also contain a __init__.py that can either 
    be left blank, or contain some code to load in each of the modules into a class structure or a wrapper function that calls what subfunctions are 
    needed.
Option 3:
    While not a folder structure, it is possible to use this folder for things like class definitions, unit testing protocols, and common aspects such
    as plotting. Think of this folder as where any computations can lie where as the routes folder only contains the IO between the user and the 
    calculations.

This folder will contain the most relivant engineering and IP related work. Aspects of this might be able to be hidden with proper programming to 
protect IP/License stakeholder's interests.
"""