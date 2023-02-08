#!/bin/sh
set -x
if [ ! -e reports ]; then
    mkdir reports
fi
python -m coverage run --include='pypog/*' -m pytest --junitxml=reports/junit.xml --html=reports/tests.html
python -m coverage xml -o reports/coverage.xml
python -m coverage html -d reports/coverage
genbadge tests -i reports/junit.xml -o reports/tests.svg
genbadge coverage -i reports/coverage.xml -o reports/coverage.svg
rm reports/coverage.xml reports/junit.xml .coverage
