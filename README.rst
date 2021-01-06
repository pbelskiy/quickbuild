Python client for `QuickBuild <https://www.pmease.com/quickbuild>`_
===================================================================

Status
------

|Build status|
|Docs status|
|Coverage status|
|Version status|
|Downloads status|

.. |Build status|
   image:: https://github.com/pbelskiy/quickbuild/workflows/Tests/badge.svg
.. |Docs status|
   image:: https://readthedocs.org/projects/quickbuild/badge/?version=latest
.. |Coverage status|
   image:: https://img.shields.io/coveralls/github/pbelskiy/quickbuild?label=Coverage
.. |Version status|
   image:: https://img.shields.io/pypi/pyversions/quickbuild?label=Python
.. |Downloads status|
   image:: https://img.shields.io/pypi/dm/quickbuild?color=1&label=Downloads

Documentation
-------------

`Read the Docs <https://quickbuild.readthedocs.io/en/latest/>`_

Installation
------------

::

    pip3 install quickbuild

Examples
--------

Get server version:

.. code:: python

    from quickbuild import QBClient

    client = QBClient('http://server', 'login', 'password')
    version = client.get_version()
    print(version)

With async client:

.. code:: python

    import asyncio
    from quickbuild import AsyncQBClient

    client = AsyncQBClient('http://server', 'login', 'password')

    async def example():
        await client.get_version()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(example())
    finally:
        loop.run_until_complete(client.close())
        loop.close()

Testing
-------

Prerequisites: `tox`

Then just run tox, all dependencies and checks will run automatically

::

    tox

Contributing
------------

Feel free for contributions

`Official REST API documentation <https://wiki.pmease.com/display/QB10/RESTful+API>`_
-------------------------------------------------------------------------------------
