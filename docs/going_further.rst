Going Further
=============


Why Slight?
-----------

We needed a very small tool to host and edit our slideshows. We wanted both the
simplicity of an tiny online editor and the full power of hand-made HTML and
CSS. We were very appealed by the possibility to reuse different themes for our
slideshows, to store and version our presentations, but not to mix everything.

That’s why we created Slight.

A small piece of software made with Python, JavaScript, HTML, CSS. No more than
200 lines of each. Of course, to achieve this, Slight uses incredible libraries
such as `reveal.js`_, Flask_ and WeasyPrint_.

.. _reveal.js: https://revealjs.com/
.. _Flask: https://flask.palletsprojects.com/
.. _WeasyPrint: https://weasyprint.org/


Content Structure
-----------------

Slideshows
~~~~~~~~~~

Each slideshow is stored in a folder whose is the name of the slideshow.
The folder contains at least 2 files.

``meta.html`` contains metadata, such as the theme and the title of the
slideshow. You can also add some HTML tags to this file (other metadata, but
also JavaScript and CSS), they will be included in the header.

``slides.html`` contains the slides, each slide being ``section`` tag. You can
also edit this file using your favorite editor, as long as this file remains
only a list of ``section`` elements.

You can also add a ``static`` folder where you can store extra static files,
including images. These files can be accessed using the relative
``static/file.ext`` URL in your HTML files.

These slideshows can easily be versioned. You can also store them in
multiple repositories and list them all in one unique Slight session using
multiple ``-s`` options.

Themes
~~~~~~

Each theme is stored in a folder whose name is the name of the theme. The
folder contains a ``style.css`` file including the stylesheet. You can also
include other static files such as images, and reference them in the stylesheet
using their filenames as URL.

As slideshows, themes can be easily versioned. And as slideshows, you can
store them in multiple repositories and use multiple ``-t`` options.
