First Steps
===========


Install
-------

The easiest way to use Slight is to clone its repository and install it in a
Python `virtual environment`_::

    git clone https://github.com/CourtBouillon/slight.git --recurse-submodules
    cd slight
    python -m venv venv
    venv/bin/pip install -e .

These lines will download and install everything needed for Slight, including
the Python dependencies and reveal.js.

.. _virtual environment: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/


Launch
------

To launch Slight, you first have to create a folder for :ref:`slideshows` and a
folder for :ref:`themes`::

    mkdir slideshows
    mkdir themes
    mkdir themes/demo
    echo "body { color: blue }" > themes/demo/style.css

When these folders have been created, you can launch Slight::

    venv/bin/slight -s slideshows -t themes

You can then visit `<http://localhost:5000/>`_ with your favourite browser and
start creating and editing your slideshows. They will be stored in the
``slideshows`` folder.

You can later edit the ``themes/demo/style.css`` stylesheet with your favorite
editor to get a beautiful slideshow. You can also create new themes and put
them in the ``themes`` folder.
