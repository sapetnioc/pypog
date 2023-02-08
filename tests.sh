#!/bin/sh
python -m coverage run --include='pypog/*' -m pytest --junitxml=junit.xml
python -m coverage xml
genbadge tests -i junit.xml -o tests.svg
genbadge coverage -i coverage.xml -o coverage.svg
rm coverage.xml junit.xml .coverage
 


