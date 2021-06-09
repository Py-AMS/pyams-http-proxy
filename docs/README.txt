========================
PyAMS HTTP proxy package
========================

.. contents::


What is PyAMS?
==============

PyAMS (Pyramid Application Management Suite) is a small suite of packages written for applications
and content management with the Pyramid framework.

**PyAMS** is actually mainly used to manage web sites through content management applications (CMS,
see PyAMS_content package), but many features are generic and can be used inside any kind of web
application.

All PyAMS documentation is available on `ReadTheDocs <https://pyams.readthedocs.io>`_; source code
is available on `Gitlab <https://gitlab.com/pyams>`_ and pushed to `Github
<https://github.com/py-ams>`_. Doctests are available in the *doctests* source folder.


What is PyAMS HTTP proxy?
=========================

PyAMS HTTP proxy is a small package which can be used to create an application proxy.

This package is using AsyncIO with Starlette and is not supposed to be used with Pyramid, but
with another ASGI compatible server like GUnicorn.

The package is based on plug-ins which can be used to handle different tasks; very few plug-ins
are actually available, to handle tasks like logging, Elasticsearch requests indexing or
JSON body rewrites...
