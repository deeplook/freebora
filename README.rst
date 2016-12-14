Fetch Free O'Reilly eBooks
==========================

.. image:: header.png
    :width: 100 %
    :align: center
		    
This is a tool for downloading free O'Reilly ebooks of different categories,
see http://shop.oreilly.com/category/ebooks.do.

This is not using ``scrapy`` on purpose (partly to avoid a configuration fest)
and is implemented in two phases:

1. crawling O'Reilly online shop to compile a list of URLs for PDF files 
   to download, and
2. downloading all files from the list created in 1.

Step 1 is done sequentially (for now), while for step 2 you can choose
between a sequential and a parallel version using 'requests' and 'aiohttp',
respectively.

See the files ``session1.txt``, ``session2.txt`` and ``session3.txt`` in the
``docs/sessions`` folder for some use-cases of varying sizes.


Installation
------------

You can install ``freebora`` with a simple ``pip install freebora`` from
the Python Package Index, or after cloning or downloading this code from
GitHub and running ``python3 setup.py install`` in its root directory.
At the moment it is intended to work only on Python 3.


Tests
-----

You can run the (pretty small) test suite like this:

.. code-block:: console

    # using py.test (needs a pip install pytest):
    py.test -v tests

    # using a minified version of py.test, included in runtests.py:
    python3 setup.py test

Individual tests can be run like this:

.. code-block:: console

    py.test -s tests/test_oreilly_shop.py


Todo
----

- add an async version of the function to collect URLs (step 1 above)
- improve command-line interface
- add feature to download not only PDFs, but other formats, too
- add feature to interactively select individual ebooks to download
