# ckanext-latex

Adds LaTEX scheming display and form snippets for CKAN forms.

## Requirements

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | yes           |

## Installation

Use pypi to install the package:

    pip install ckanext-latex


## Developer installation

To install ckanext-latex for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/mutantsan/ckanext-latex.git
    cd ckanext-latex
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
