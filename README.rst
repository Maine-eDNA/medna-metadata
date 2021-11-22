===================
Maine-eDNA Metadata
===================
.. image:: https://readthedocs.org/projects/medna-metadata/badge/?version=latest
  :target: https://medna-metadata.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

Support for this project is provided through a National Science Foundation award to `Maine EPSCoR at the University of
Maine <https://umaine.edu/edna/>`__ and is part of the RII Track-1: Molecule to Ecosystem: Environmental DNA as a Nexus
of Coastal Ecosystem Sustainability for Maine (Maine-eDNA).

This repository contains the backend components of Maine-eDNA metadata (API, database) and was built with the `Django web
framework <https://www.djangoproject.com/>`__. The frontend components are located in the `medna-metadata-frontend
repository <https://github.com/Maine-eDNA/medna-metadata-frontend>`__, which is written with the
`ReactJS library <https://reactjs.org/>`__. The frontend communicates with the backend through the API, built with the
`Django REST Framework <https://www.django-rest-framework.org/>`__.

.. note::
    The Dockerfiles in ``/docker`` are **not fully tested**. Once they have been this message will be updated and users
    can use the docker steps to deploy the django app.

Documentation & Setup
---------------------

- **Read the Docs**: https://medna-metadata.readthedocs.io/en/latest/

Related Repositories and Projects
---------------------------------

- **medna-metadata-frontend**: https://github.com/Maine-eDNA/medna-metadata-frontend


Contributors
------------
.. image:: https://contrib.rocks/image?repo=Maine-eDNA/medna-metadata
   :target: https://github.com/Maine-eDNA/medna-metadata/graphs/contributors
   :alt: Repository Contributors

Made with `contributors-img <https://contrib.rocks>`__.
