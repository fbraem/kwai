#!/bin/bash
rm -rf ./kwai
rm -rf ./tests
poetry -C ../src run sphinx-apidoc -e -o ./kwai ../src/kwai
poetry -C ../src run sphinx-apidoc -e -o ./tests ../src/tests
make html
