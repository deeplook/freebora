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

See the files ``session1.txt``, ``session2.txt`` and ``session3.txt`` for some
use-cases of varying sizes.

Todo:

- package nicely using ``distutils``
- add an async version of the function to collect URLs (step 1 above)
- improve command-line interface
- add feature to download not only PDFs, but other formats, too
- add feature to list all available ebook category names
