#For setuptools
import ez_setup

ez_setup.use_setuptools()

from setuptools import setup, find_packages
setup(
	name = "BeyondPartyLines",
	version = "0.1",
	packages = find_packages(),
	scripts = ['beyondpartylines.py'],

	install_requires = ['numpy>=1.5.1','matplotlib>=1.0.1','pyttk>=0.3.2','BeautifulSoup>=3.2.0'],

	package_data = {
		'' : ['README','LICENSE','currentsitting.dat']
	},

	author = "Wilson Brenna",
	author_email = "wbrenna@uwaterloo.ca",
	description = "Vote along with the Canadian House of Commons!",
	url = "http://github.com/wbrenna/beyondpartylines"
)
