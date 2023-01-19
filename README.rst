Python client for PMEase `QuickBuild <https://www.pmease.com/quickbuild>`_
==========================================================================

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

----

Package supports sync and async syntax with same code base.

.. code:: python

    from quickbuild import AsyncQBClient, QBClient

Documentation
-------------

`Package Read the Docs <https://quickbuild.readthedocs.io/en/latest/>`_

`Official REST API documentation <https://wiki.pmease.com/display/QB12/RESTful+API>`_

`Available REST API Clients <https://wiki.pmease.com/display/QB12/Available+Clients>`_

Installation
------------

.. code:: shell

    pip3 install quickbuild

Examples
--------

Get server version:

.. code:: python

    from quickbuild import QBClient

    client = QBClient('https://server', 'user', 'password')
    version = client.system.get_version()
    print(version)

Get server version in async way (be careful ``AsyncQBClient`` must be called inside async function):

.. code:: python

    import asyncio
    from quickbuild import AsyncQBClient

    async def main():
        client = AsyncQBClient('https://server', 'user', 'password')
        version = await client.system.get_version()
        print(version)
        await client.close()

    asyncio.run(main())

Stop build:

.. code:: python

    from quickbuild import QBClient

    client = QBClient('https://server', 'user', 'password')
    client.builds.stop(123)


Update credentials handler:

.. code:: python

    import asyncio
    import aiohttp
    from quickbuild import AsyncQBClient

    async def get_credentials():
        async with aiohttp.ClientSession() as session:
            async with session.get('...') as resp:
                response = await resp.json()
                return response['user'], response['password']

    async def main():
        client = AsyncQBClient('http://server', 'user', 'password',
                                auth_update_callback=get_credentials)

        # let's suppose credentials are valid now
        print(await client.builds.get_status(12345))

        # now, after some time, password of user somehow changed, so our callback
        # will be called, new credentials will be using for retry and future here
        # we get also correct build info instead of QBUnauthorizedError exception
        print(await client.builds.get_status(12345))

        await client.close()

    asyncio.run(main())


Content type
------------

By default QuickBuild returns XML content, but starting from 10 version it also
has native support of JSON content, usually it's much more convenient to use
native Python types (parsed XML) instead of pure XML string.

So, that is why three types of content were indtoduced, this type and behavior
can be set globally for client instances, and can be rewritten for some methods.

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
