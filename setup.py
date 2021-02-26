import os
import re

from setuptools import setup, find_packages

init_file_path = os.path.join(
    os.path.dirname(__file__),
    'quickbuild/__init__.py'
)

with open(init_file_path) as f:
    try:
        version = re.findall(r"__version__ = '(.*)'", f.read())[0]
    except IndexError:
        raise RuntimeError('Unable to get package version')

with open('README.rst') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='quickbuild',
    version=version,
    description='Python client for PMEase QuickBuild',
    long_description_content_type='text/x-rst',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    license='MIT',
    packages=find_packages(),
    package_data={'quickbuild': ['*']},
    author='Petr Belskiy',
    author_email='petr.belskiy@gmail.com',
    keywords=['PMEase', 'quickbuild'],
    url='https://github.com/pbelskiy/quickbuild',
    download_url='https://pypi.org/project/quickbuild'
)

install_requires = [
    'aiohttp>3.6.2,<4.0.0',
    'requests>=2.24.0,<3.0.0',
    'xmltodict==0.12',
]

setup(
    install_requires=install_requires,
    python_requires='>=3.5',
    **setup_args
)
