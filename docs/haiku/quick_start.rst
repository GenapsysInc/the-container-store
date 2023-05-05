Quick Start
***********

Initial Setup
=============

* Install `Docker Desktop <https://www.docker.com/products/docker-desktop/>`_
* Install `GitHub Desktop <https://desktop.github.com/>`_ or command-line git commands

Clone Haiku code (if developing)
--------------------------------

* Clone ``the-container-store`` repository via command-line or GitHub Desktop

  * GitHub Desktop
    * Login with your github account via the GitHub.com button
    * Search for the ``the-container-store`` repository and select clone

  * Command line
    .. code-block::

      git clone git@github.com:open-reading-frame/the-container-store.git

* From the `the-container-store` directory run `make haiku-img`. This step will take time to run the first time.

.. code-block::

   gsmac00:the-container-store$ make haiku

Pull haiku docker (if not developing)
-------------------------------------

.. code-block::

   docker pull ghcr.io/open-reading-frame/haiku:latest

.. note:: You can replace `latest` with a specific version number if you want to pull a legacy version.


Running Jupyter in Haiku
========================

* Start the docker container

  * If using the development you can run `make haiku-env`
  * You can use the following command to run the docker directly

    .. code-block::

       docker run -it --platform linux/x86_64 -p 8888:8888 -v </LOCAL/PATH/TO/NOTEBOOKS>:/notebooks/ haiku:latest

    .. note::
       To make local data available to the docker container add `-v <LOCAL/PATH/TO/DATA>:/data`

* At the haiku prompt run `jupyter`.

.. code-block::

  [root@0fb1c465f678 /]# jupyter
  [I 20:17:07.149 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
  [I 20:17:07.876 NotebookApp] Serving notebooks from local directory: /
  [I 20:17:07.876 NotebookApp] Jupyter Notebook 6.5.2 is running at:
  [I 20:17:07.876 NotebookApp] http://0fb1c465f678:8888/?token=b316ec5137f4b25ecd63a3a0fe0aaab64d1b6db1a71e014b
  [I 20:17:07.877 NotebookApp]  or http://127.0.0.1:8888/?token=b316ec5137f4b25ecd63a3a0fe0aaab64d1b6db1a71e014b
  [I 20:17:07.877 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
  [C 20:17:07.896 NotebookApp]

      To access the notebook, open this file in a browser:
          file:///root/.local/share/jupyter/runtime/nbserver-38-open.html
      Or copy and paste one of these URLs:
          http://0fb1c465f678:8888/?token=b316ec5137f4b25ecd63a3a0fe0aaab64d1b6db1a71e014b
       or http://127.0.0.1:8888/?token=b316ec5137f4b25ecd63a3a0fe0aaab64d1b6db1a71e014b


* Paste the last link with the `127.0.0.1` into the browser of you choice
* Jupyter should be running now

   * Notebooks included with Haiku will be in the /notebooks directory.
   * Any other notebooks or data need to be shared with the docker container via a bind mount

.. note:: If the jupyter kernel repeatedly dies you will need to increase the memory provided to the docker container

General Items
=============

* `exit` will exit out of an interactive docker session
* Bind mounts can be added to the make command with the MOUNT option

  .. code-block::

     MOUNT="-v /Local/Path/to/some_data/:/data/"
     Or for multiple mounts
     MOUNT="-v /Local/Path/to/some_data/:/data/ -v /Local/Path/to/some_code/:/code/local/"


Troubleshooting
===============

There is already a haiku container running::

  docker: Error response from daemon: driver failed programming external connectivity on endpoint peaceful_poincare (f32ac02786bfe9e4b4e07a1b45ca1120c32d9dc6d15926fa685338398f532514): Bind for 0.0.0.0:8888 failed: port is already allocated.
