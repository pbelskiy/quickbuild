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

Features
--------

.. list-table:: QuickBuild RESTful API support
  :widths: 80 20

  * - API
    - Supported?
  * - `Interact with Audits <https://wiki.pmease.com/display/QB10/Interact+with+Audits>`_
    - no
  * - `Interact with Configurations <https://wiki.pmease.com/display/QB10/Interact+with+Configurations>`_
    - no
  * - `Interact with Builds <https://wiki.pmease.com/display/QB10/Interact+with+Builds>`_
    - yes
  * - `Interact with Latest Builds <https://wiki.pmease.com/display/QB10/Interact+with+Latest+Builds>`_
    - no
  * - `Interact with Build Requests <https://wiki.pmease.com/display/QB10/Interact+with+Build+Requests>`_
    - no
  * - `Trigger Build via GET Request <https://wiki.pmease.com/display/QB10/Trigger+Build+via+GET+Request>`_
    - no
  * - `Interact with Users <https://wiki.pmease.com/display/QB10/Interact+with+Users>`_
    - yes
  * - `Interact with Groups <https://wiki.pmease.com/display/QB10/Interact+with+Groups>`_
    - no
  * - `Interact with Group Memberships <https://wiki.pmease.com/display/QB10/Interact+with+Group+Memberships>`_
    - no
  * - `Interact with Dashboards <https://wiki.pmease.com/display/QB10/Interact+with+Dashboards>`_
    - no
  * - `Interact with Group Share <https://wiki.pmease.com/display/QB10/Interact+with+Group+Share>`_
    - no
  * - `Interact with User Share <https://wiki.pmease.com/display/QB10/Interact+with+User+Share>`_
    - no
  * - `Interact with Cloud Profiles <https://wiki.pmease.com/display/QB10/Interact+with+Cloud+Profiles>`_
    - no
  * - `Interact with Configuration Authorizations <https://wiki.pmease.com/display/QB10/Interact+with+Configuration+Authorizations>`_
    - no
  * - `Interact with Resources <https://wiki.pmease.com/display/QB10/Interact+with+Resources>`_
    - no
  * - `Interact with Agent Tokens <https://wiki.pmease.com/display/QB10/Interact+with+Agent+Tokens>`_
    - no
  * - `Get System Attributes of Grid Node <https://wiki.pmease.com/display/QB10/Get+System+Attributes+of+Grid+Node>`_
    - no
  * - `Get and Set User Attributes of Grid Node <https://wiki.pmease.com/display/QB10/Get+and+Set+User+Attributes+of+Grid+Node>`_
    - no
  * - `Interact with Reports <https://wiki.pmease.com/display/QB10/Interact+with+Reports>`_
    - no
  * - `Interact with Changes <https://wiki.pmease.com/display/QB10/Interact+with+Changes>`_
    - no
  * - `Interact with Issues <https://wiki.pmease.com/display/QB10/Interact+with+Issues>`_
    - no
  * - `Query Build Notifications <https://wiki.pmease.com/display/QB10/Query+Build+Notifications>`_
    - no
  * - `Query Grid Measurements <https://wiki.pmease.com/display/QB10/Query+Grid+Measurements>`_
    - no
  * - `Access Information of Published Files <https://wiki.pmease.com/display/QB10/Access+Information+of+Published+Files>`_
    - no
  * - `Interact with Build Agents <https://wiki.pmease.com/display/QB10/Interact+with+Build+Agents>`_
    - no
  * - `Backup Database <https://wiki.pmease.com/display/QB10/Backup+Database>`_
    - no
  * - `Pause System <https://wiki.pmease.com/display/QB10/Pause+System>`_
    - no
  * - `Resume System <https://wiki.pmease.com/display/QB10/Resume+System>`_
    - no
  * - `Check System Pause Information <https://wiki.pmease.com/display/QB10/Check+System+Pause+Information>`_
    - no
  * - `Retrieve Object Identifier <https://wiki.pmease.com/display/QB10/Retrieve+Object+Identifier>`_
    - no

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
