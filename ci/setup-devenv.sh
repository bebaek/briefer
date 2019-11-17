#!/bin/bash
# Set up development env.

echo Start: set up Python environment.

devenv=briefer
pkgs=(flake8 ipython ruamel.yaml)

# Install edm
# FIXME: implement

# Create edm env
edm env remove -y $devenv
edm env create --version 3 $devenv

# Install Python packages
if [ ${#pkgs[@]} -ne 0 ]; then
    edm install -e $devenv -y ${pkgs[@]}
fi

echo End: set up Python environment.
