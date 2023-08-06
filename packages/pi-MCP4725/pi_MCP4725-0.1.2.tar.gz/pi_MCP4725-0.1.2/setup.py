from distutils.core import setup

# read the contents of your description file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "DESC.md").read_text()


setup(
	name = 'pi_MCP4725',         # How you named your package folder (MyLib)
	packages = ['pi_MCP4725'],   # Chose the same as "name"
	version = '0.1.2',      # Start with a small number and increase it with every change you make
	license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
	description = 'Python module to use the MCP4725 DAC with the Raspberry Pi',   # Give a short description about your library
	long_description = long_description,
	long_description_content_type='text/markdown',
	author = 'Sergio Caponi',                   # Type in your name
	author_email = 'contactme@sergiocaponi.com',      # Type in your E-Mail
	url = 'https://github.com/sergiocaponi/pi_MCP4725',   # Provide either the link to your github or to your website
	download_url = 'https://github.com/sergiocaponi/pi_MCP4725/archive/refs/tags/v0.1.2.tar.gz',    # I explain this later on
	keywords = ['Raspberry Pi', 'DAC', 'MCP4725'],   # Keywords that define your package best
	install_requires=[            # I get to this in a second
					'smbus2',
			],
	classifiers=[
		'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
		'Intended Audience :: Developers',      # Define that your audience are developers
		'Operating System :: POSIX :: Linux',
		'Topic :: Software Development :: Build Tools',
		'Topic :: System :: Hardware',
		'License :: OSI Approved :: MIT License',   # Again, pick a license
		'Programming Language :: Python :: 3',
	],
)