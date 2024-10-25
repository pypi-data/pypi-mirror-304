[![Tests](https://github.com/DataShades/ckanext-js-tweaks/workflows/Tests/badge.svg?branch=main)](https://github.com/DataShades/ckanext-js-tweaks/actions)

# ckanext-js-tweaks

It's a bunch of scripts, macroses and helpers to make daily routing easier.

### Adding tooltip
Just add `data-tooltip="text"` attribute to an element to display basic tooltip.

OR use bootstrap tooltips, if you want.
`data-toggle="tooltip" data-placement="top" title="Tooltip on top"`


## Installation

**TODO:** Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-js-tweaks:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/DataShades/ckanext-js-tweaks.git
    cd ckanext-js-tweaks
    pip install -e .
	pip install -r requirements.txt

3. Add `js-tweaks` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

None at present

**TODO:** Document any optional config settings here. For example:

	# The minimum number of hours to wait before re-checking a resource
	# (optional, default: 24).
	ckanext.js_tweaks.some_setting = some_default_value


## Developer installation

To install ckanext-js-tweaks for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/DataShades/ckanext-js-tweaks.git
    cd ckanext-js-tweaks
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
