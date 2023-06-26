Installation
============

Installing Dragon Mapper is easy. You can use
`pip <https://pip.pypa.io>`_:

.. code:: bash

    $ pip install dragonmapper

That will download Dragon Mapper from
`the Python Package Index <https://pypi.python.org/>`_ and install it in your
Python's ``site-packages`` directory.

Tarball Release
---------------

If you'd rather install Dragon Mapper manually:

1. Download the most recent release from `Dragon Mapper's PyPi page <https://pypi.python.org/pypi/dragonmapper/>`_.
2. Unpack the tarball.
3. From inside the directory ``dragonmapper-XX``, run ``pip install .``

That will install Dragon Mapper in your Python's ``site-packages`` directory.

Install the Development Version
-------------------------------

`Dragon Mapper's code <https://github.com/tsroten/dragonmapper>`_ is hosted at GitHub.
To install the development version first make sure `Git <https://git-scm.org/>`_
is installed. Then run:

.. code-block:: bash
   
    $ git clone git://github.com/tsroten/dragonmapper.git
    $ pip install -e dragonmapper

This will link the ``dragonmapper`` directory into your ``site-packages``
directory.

Running the Tests
-----------------

Running the tests is easy. Make sure you have `hatch <https://hatch.pypa.io>`_
installed.

.. code-block:: bash

    $ hatch run test
