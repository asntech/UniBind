UniBind
=======

UniBind is a comprehensive database of transcription factor binding sites predicted through uniform processing of thousands of ChIP-seq datasets by using three different peak callers and five different prediction models.

This is the source code of UniBind website developed in Python/Django. To run the website locally, you need to install Django and a list of other Python packages which are listed in the requirements.txt file.


Get the development version from `Bitbucket`
--------------------------------------------

If you have `git` and `pip` installed, use this:

.. code-block:: bash

    git clone https://bitbucket.org/CBGR/UniBind.git
    cd UniBind
    pip install -r requirements.txt
    python manage.py runserver

Then copy the following URL in your browser.

.. code-block:: bash

    http://127.0.0.1:8000/


To deploy the app on a server with Apache and mod_wsgi please read this https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/modwsgi/​​

