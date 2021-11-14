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

`Official REST API documentation <https://wiki.pmease.com/display/QB10/RESTful+API>`_

Installation
------------

::

    pip3 install -U quickbuild

Examples
--------

Get server version:

.. code:: python

    from quickbuild import QBClient

    client = QBClient('http://server', 'login', 'password')
    version = client.system.get_version()
    print(version)

With async client:

.. code:: python

    import asyncio
    from quickbuild import AsyncQBClient

    client = AsyncQBClient('http://server', 'login', 'password')

    async def example():
        await client.system.get_version()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(example())
    finally:
        loop.run_until_complete(client.close())
        loop.close()

Content type
------------

By default QuickBuild returns XML content, but starting from 10 version it also
has native support of JSON content, usually it's much more convenient to use
native Python types (parsed XML) instead of pure XML string.

So, that is why current package introducing three types of content, this type and
behavior can be set globally for client instances, and can be rewritten for some
methods.

- PARSE (using by default)
    - GET: parse XML to native Python types.
    - POST: pure XML string.

- XML
    - GET: return native XML without any transformations.
    - POST: pure XML string.

- JSON (QuickBuild 10+)
    - GET: parsed JSON string.
    - POST: dumps object to JSON string.

Development
-----------

It's possible to run QuickBuild community edition locally using docker:

Build locally:

.. code:: shell

    docker build .  -f docker/QB10.Dockerfile -t quickbuild:10
    docker run --restart always --name qb10 -d -p 8810:8810 quickbuild:10

Or run prepared image:

.. code:: shell

    docker run --restart always --name qb10 -d -p 8810:8810 pbelskiy/quickbuild:10

Then open http://localhost:8810/

Testing
-------

Prerequisites: `tox`

Then just run tox, all dependencies and checks will run automatically

::

    tox

Contributing
------------

Feel free for any contributions.
