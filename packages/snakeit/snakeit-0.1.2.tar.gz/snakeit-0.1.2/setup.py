from distutils.core import setup

from snakeit import __version__


setup(
	name		 = 'snakeit',
	packages	 = ['snakeit'],
	version		 = __version__,
	license		 = 'MIT',
	description  = 'A one-file-script named `snakeit` that build wrappers for c++ classes.',
	author		 = 'kaalam',
	author_email = 'kaalam@kaalam.ai',
	url			 = 'https://github.com/kaalam/snakeit',
	download_url = 'https://github.com/kaalam/snakeit/dist/snakeit-%s.tar.gz' % __version__,
	keywords	 = ['utilities', 'c++'],
	scripts		 = ['bin/snakeit'],
	classifiers  = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3']
)
