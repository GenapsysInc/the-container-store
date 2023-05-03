*******************************
Coding Standards and Guidelines
*******************************


Python
++++++

  * Use of an IDE is recommended as the development/debugging environment
  * Use 4 spaces for indentation not tabs.

Docstrings
----------
  * All functions must have a docstring where the inputs and outputs are clearly described in terms of data type and description
  * PEP8 documentation with reStructuredText for docstrings

Example:
    .. code-block:: python

        def some_function(input_path, magic_number=42):
            """
            This is a function that is used for documentation
            :param str input_path: Path of the input
            :param int magic_number: The magic number used in the function
            :returns: int
            """
            pass


Object Naming
-------------

  * Variables, functions, methods, packages, modules: `this_is_a_variable`
  * Classes and exceptions: `CapWords`
  * Protected methods and internal functions: `_single_leading_underscore`
  * Private methods: `__double_leading_underscore`
  * Constants: `CAPS_WITH_UNDERSCORES`

    * Define constants underneath the import statements. A well named constant (e.g. MAX_ITERATIONS_DEFAULT)  is much better than a magic number in the code.

Imports
-------

Imports are always at the top starting from imports from native python a blank line 3rd library imports a blank line and then internal code imports.

.. code-block:: python

   import sys
   import os

   import numpy

   import local.library




Plotting
--------


Other
-----

  * Logs must be concise and informative.
  * Avoid putting log messages in for loops. Examine the output Log file to make sure log messages are concise.
  * The final code should not contain any unused variables or commented out code
  * Avoid using a single character (i, j, n, q...) variable in blocks of code that extends over a large number of lines.
  * Do not name a variable with the same identifier string as one of the built in types or functions.
  * Lines should not exceed the limit of 120 characters.
  * Operations using “random” should set the “seed” to make the results repeatable.
  * Analysis functions and modules should only operate on data presented to them.  They should not directly access data from filestorage, databases or other raw sources
  * Utility functions should be reused and made more generic as use cases increase, instead of adding similar functions.
  * Be aware of backwards-compatibility considerations while modifying existing functions/methods. Make sure to address all the instances/calls in case of changes in the input/out arguments

Jupyter
+++++++



