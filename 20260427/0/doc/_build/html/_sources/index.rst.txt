.. first proj documentation master file, created by
   sphinx-quickstart on Mon Apr  6 13:16:38 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

first proj documentation
========================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.

The script
========================

.. literalinclude:: ../restcalend/__main__.py

This *is* the **text**

The calendar
========================

.. include:: calend.rst

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   API
