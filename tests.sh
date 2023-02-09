#!/bin/sh
branch='main_reports'
if ! echo "$branch"| grep -Eq '.*_reports$'; then
    echo go
else
    echo no
fi
# if [ ! -e reports ]; then
#     mkdir reports
# fi
# python -m coverage run --source=. -m pytest --junitxml=reports/junit.xml --html=reports/tests.html
# python -m coverage html -d reports/coverage
# python -m coverage xml -o reports/coverage.xml
# genbadge tests -i reports/junit.xml -o reports/tests.svg
# genbadge coverage -i reports/coverage.xml -o reports/coverage.svg
# rm reports/coverage.xml reports/junit.xml .coverage
