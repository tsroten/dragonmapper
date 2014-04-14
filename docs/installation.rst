Installation
============

Installing Dragon Mapper is easy. Make sure you have Python 2.7 or 3 along
with `Zhon <https://github.com/tsroten/zhon>`_ and
`Hanzi Identifier <https://github.com/tsroten/hanzidentifier>`_. Then use
`pip <http://www.pip-installer.org/>`_:

.. code:: bash

    $ pip install dragonmapper

That will download Dragon Mapper from
`the Python Package Index <http://pypi.python.org/>`_ and install it in your
Python's ``site-packages`` directory.

Tarball Release
---------------

If you'd rather install Dragon Mapper manually:

1.  Download the most recent release from `Dragon Mapper's PyPi page <http://pypi.python.org/pypi/dragonmapper/>`_.
2. Unpack the tarball.
3. From inside the directory ``dragonmapper-XX``, run ``python setup.py install``

That will install Dragon Mapper in your Python's ``site-packages`` directory.

Install the Development Version
-------------------------------

`Dragon Mapper's code <https://github.com/tsroten/dragonmapper>`_ is hosted at GitHub.
To install the development version first make sure `Git <http://git-scm.org/>`_
is installed. Then run:

.. code-block:: bash
   
    $ git clone git://github.com/tsroten/dragonmapper.git
    $ pip install -e dragonmapper

This will link the ``dragonmapper`` directory into your ``site-packages``
directory.

Running the Tests
-----------------

Running the tests is easy:

.. code-block:: bash

    $ python setup.py test

If you want to run the tests using multiple versions of Python, install and
run tox:

.. code-block:: bash

    $ pip install tox
    $ tox

Dragon Mapper's ``tox.ini`` file is configured to run tests using Python 2.7, 3.3,
and 3.4. It will also build the documentation (requires
`Sphinx <http://sphinx-doc.org>`_).
