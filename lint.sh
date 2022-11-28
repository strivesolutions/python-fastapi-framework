#!/bin/sh

set -e
package=fastapiframework


echo "Flake8 error count:"
flake8 $package tests --count --show-source --statistics
echo "iSort results:"
isort --check $package --profile black
echo "ok" # won't get here if the previous step fails
isort --check tests
echo "MyPy results:"
mypy $package