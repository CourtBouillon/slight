API Reference
=============

.. currentmodule:: slight

This page is for Slight |version|. See :doc:`changelog </changelog>` for
older versions.


Command-line API
----------------

.. autofunction:: slight.__main__.main(argv=sys.argv)


Environment Variables
---------------------

When you don’t launch Slight using the ``slight`` executable, for example
behind an :ref:`HTTP server`, you can use the ``SLIGHT_SLIDESHOWS`` and
``SLIGHT_THEMES`` environment variables to set the folders where your slides
and themes are stored.

Multiple paths are separated by ``:``.
