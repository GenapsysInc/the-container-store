Contributions
#############

Contributions must be made via pull request to the `main` branch.

All code should have documentation, unit tests and follow the coding guidelines.

Python < 3.6 is not allowed or supported.

Adding Tools
============

  * Python libraries should be added to the `haiku/python_requirements.txt`
  * Third party tools available via yum should be added to the `haiku/yum_requirements.txt`
  * Third party tools that require custom installation should have an installation script added to the `haiku/dependencies/scripts/` directory.  The script filename must start with `install_` in order to be executed correctly

Third party tools or python libraries that can be executed directly should be documented in `docs/haiku/tools.rst`

.. Documentation
.. =============

.. This tool is auto documented including code api docs on every merge to main.
.. No code right now so leaving this commented out
