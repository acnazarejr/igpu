"""Setup script."""

from setuptools import setup

VERSION = '0.1.0'
AUTHOR = 'Antonio Carlos Nazare Jr.'
EMAIL = 'antonio.nazare@dcc.ufmg.br'
REQUIREMENTS = [line for line in open('requirements.txt').read().split('\n') if line != '']

setup(
    name='igpu',
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    url='http://github.com/acnazarejr/igpu',
    download_url='http://github.com/acnazarejr/igpu',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    description='A cross-platform module for retrieving information and stats on installed gpus.',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    keywords='gpu cuda nvidia',
    packages=['igpu'],
    zip_safe=False,
    python_requires='>=3.4',
    install_requires=REQUIREMENTS
)
