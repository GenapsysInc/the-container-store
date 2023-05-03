#!/bin/bash
set -x

# Based on https://github.com/annegentle/create-demo


pip3 install Sphinx sphinx_rtd_theme mlx.traceability



##############
# BUILD DOCS #
##############

# Python Sphinx, configured with source/conf.py
# See https://www.sphinx-doc.org/
make clean
make html


