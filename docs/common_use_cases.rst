Common Use Cases
================


PDF Export
----------

Slideshows can be exported in PDF using the corresponding icon on the
edition page. Export is done by WeasyPrint_ that should be installed
automatically with Slight.

If you get errors while generating your slideshows, please take a look at
`WeasyPrint’s documentation`_ that includes an installation guide and a
troubleshooting section.

.. _WeasyPrint: https://weasyprint.org/
.. _WeasyPrint’s documentation: https://doc.courtbouillon.org/weasyprint/


HTTP Server
-----------

Slight is a WSGI application based on Flask_ and can thus be put behind a
"real" HTTP server. To get information about different possibilities, you can
follow the hints provided by `Flask’s documentation`_.

If you don’t launch Slight using the ``slight`` executable, you can use
:ref:`environment variables` to set the folders where your slides and themes
are stored.

.. _Flask: https://flask.palletsprojects.com/
.. _Flask’s documentation: https://flask.palletsprojects.com/deploying/
