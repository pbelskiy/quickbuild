import os
import re

from setuptools import setup, find_packages

init_file_path = os.path.join(
    os.path.dirname(__file__),
    'quickbuild/__init__.py'
)

with open(init_file_path, encoding='utf-8') as f:
    try:
        version = re.findall(r"__version__ = '(.*)'", f.read())[0]
    except IndexError:
        raise RuntimeError('Unable to get package version')

with open('README.rst', encoding='utf-8') as f:
    README = f.read()

setup_args = dict(
    name='quickbuild',
    version=version,
    description='Python client for PMEase QuickBuild',
    long_description_content_type='text/x-rst',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    license='MIT',
    packages=find_packages(),
    package_data={'quickbuild': ['*']},
    author='Petr Belskiy',
    keywords=['PMEase', 'quickbuild'],
    url='https://github.com/pbelskiy/quickbuild',
    download_url='https://pypi.org/project/quickbuild'
)

install_requires = [
    'aiohttp>=3.6,<4',
    'requests>=2.24,<3',
    'urllib3>=1.26,<3',
    'xmltodict==0.12',
]

setup(
    install_requires=install_requires,
    python_requires='>=3.7',
    **setup_args
)
