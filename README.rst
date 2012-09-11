README for the FFM web app
===========================

:Author: Christian Tanzer <tanzer@swing.co.at>

The FFM web app is an application that serves data about the network
nodes deployed by www.funkfeuer.at.

It uses the `tapyr framework`_.

.. _`tapyr framework`: https://github.com/Tapyr/tapyr

Object model
------------

This object model (in SVG format) is automagically redered using
`graph.py`_, the result of the last run is kept under version control
(so you can see our progress) in `nodedb.svg`_.

.. _`nodedb.svg`: https://github.com/FFM/FFM/blob/master/doc/nodedb.svg
.. _`graph.py`: https://github.com/FFM/FFM/blob/master/graph.py

.. image:: https://raw.github.com/FFM/FFM/master/doc/nodedb.png
    :alt: Object model SVG
    :target: https://github.com/FFM/FFM/blob/master/doc/nodedb.svg

To render the svn to a png file with inkscape, use::

    inkscape -y 1 -e doc/nodedb.png doc/nodedb.svg

The -y option sets the background opacity, when not specified you'll get
a black background in the exported .png.

System requirements
--------------------

- Linux or OS X

  * its best to set up a separate account that runs FFM

- Apache, with mod-fcgid installed

  * or another webserver, e.g. nginx...

- PostgreSQL (preferred) or mySQL

  * an account for the web app that can create databases and tables

- git

- Python (> 2.6, < 3)

  * virtualenv, distribute

  * Depending on the OS (I'm looking at you, Debian), some packages,
    e.g., werkzeug, should be installed into virtualenv to get
    versions a bit younger than a couple of years

  * This might require the installation of a build environment (for
    python packages that need the C compiler)

- Python packages

  * `Babel`_

  * `dateutil`_

  * `docutils`_

  * `flup`_

  * `jinja2`_

  * `plumbum`_

  * `psycopg2`_ or the `mysql package`_ needed by `sqlalchemy`_

  * `pytz`_

  * `rcssmin`_, `rjsmin`_ (for minimization of CSS and Javascript files)

  * `sqlalchemy`_

  * `werkzeug`_

  All packages should be available via the `Python Package Index`_

.. _`Babel`:         http://babel.edgewall.org/
.. _`dateutil`:      http://labix.org/python-dateutil
.. _`docutils`:      http://docutils.sourceforge.net/
.. _`flup`:          http://trac.saddi.com/flup
.. _`jinja2`:        http://jinja.pocoo.org/
.. _`plumbum`:       http://plumbum.readthedocs.org/en/latest/index.html
.. _`psycopg2`:      http://packages.python.org/psycopg2/
.. _`mysql package`: http://mysql-python.sourceforge.net/
.. _`pytz`:          http://pytz.sourceforge.net/
.. _`rcssmin`:       http://opensource.perlig.de/rcssmin/
.. _`rjsmin`:        http://opensource.perlig.de/rjsmin/
.. _`sqlalchemy`:    http://www.sqlalchemy.org/
.. _`werkzeug`:      http://werkzeug.pocoo.org/
.. _`Python Package Index`: http://pypi.python.org/pypi


How to install
--------------

Assuming an account `ffm` located in /home/ffm, you'll need something
like the following::

  ### Logged in as `ffm`
  $ cd /home/ffm

  ### Define config
  $ vi .ffm.config
    ### Add the lines (using the appropriate values for **your** install)::
      cookie_salt   = 'some random value, e.g., the result of uuid.uuid4 ()'
      db_name       = "ffm"
      db_url        = "postgresql://<account>:<password>@localhost"
      languages     = "de", "en"
      locale_code   = "de"
      smtp_server   = "localhost"
      target_db_url = db_url
      time_zone     = "Mars/Olympos Mons"


  ### create a virtual environment for Python
  $ mkdir bin
  $ mkdir PVE
  $ python -m virtualenv PVE/std
  $ (cd PVE ; ln -s std active)
  $ (cd bin ; ln -s ../PVE/active/bin/python)

  ### install Python packages into the virtualenv
  ### if one of these packages is already installed in the system
  ### Python, you'll need to say `pip install --upgrade`, not `pip install`
  $ source PVE/active/bin/activate
  $ pip install Babel
  $ pip install plumbum
  $ pip install pytz
  $ pip install werkzeug

  ### create a directory with an `active` and `passive` branch of the
  ### web application
  ###
  ### * the active branch will be the one that serves apache requests
  ###
  ### * the passive branch can be used for updating the software and
  ###   testing it. It all works will the branches can be switched
  ###

  $ mkdir fcgi
  $ mkdir v
  $ mkdir v/1
  $ mkdir v/1/www
  $ mkdir v/1/www/media
  $ ln -s v/1 active
  $ ln -s v/2 passive
  $ git clone git@github.com:Tapyr/tapyr.git v/1/lib
  $ git clone git@github.com:FFM/FFM.git v/1/www/app
  $ cp -a v/1 v/2

  $ vi active/www/.ffm.config
    ### Add the lines (using the appropriate values for **your** install)::
      db_name       = "ffm1"
  $ vi passive/www/.ffm.config
      db_name       = "ffm2"

  ### Define PYTHONPATH
  $ export PYTHONPATH=/home/ffm/active/lib

  ### Create a fcgi script for Apache
  $ python active/www/app/deploy.py fcgi_script > fcgi/app_server.fcgi

  ### Configure Apache virtual host, for instance::
    <VirtualHost *:80>
      ServerName   xxx.funkfeuer.at
      DocumentRoot /home/ffm/active/www

      AddDefaultCharset utf-8

      Alias /media/GTW/ /home/ffm/active/lib/_GTW/media/
      Alias /media/     /home/ffm/active/www/media/

      <Directory /home/ffm/active/lib/_GTW/media>
        Order deny,allow
        Allow from all
        ExpiresActive On
        ExpiresDefault "access plus 1 day"
        <FilesMatch "\.(gif|jpeg|jpg|png)$">
          ExpiresDefault "access plus 1 year"
        </FilesMatch>
        <FilesMatch "\.(css|js)$">
          ExpiresDefault "access plus 1 day"
        </FilesMatch>
      </Directory>

      <Directory /home/ffm/active/www/media>
        Order deny,allow
        Allow from all
        ExpiresActive On
        ExpiresDefault "access plus 1 day"
        <FilesMatch "\.(gif|jpeg|jpg|png)$">
          ExpiresDefault "access plus 1 year"
        </FilesMatch>
        <FilesMatch "\.(css|js)$">
          ExpiresDefault "access plus 1 day"
        </FilesMatch>
        FileETag None
      </Directory>

      <Directory /home/ffm/active/www/media/v>
        ExpiresActive On
        <FilesMatch "\.(css|js)$">
          ExpiresDefault "access plus 1 year"
        </FilesMatch>
      </Directory>

      <Directory /home/ffm/active/www/media/pdf>
        FileETag all
      </Directory>

      <Directory /home/ffm/active/www/app>
        Order deny,allow
        Deny from all
      </Directory>

      AddOutputFilterByType DEFLATE text/html text/plain text/css text/javascript

      AddHandler fcgid-script .fcgi
      Options +ExecCGI

      ScriptAliasMatch .* /home/ffm/fcgi/app_server.fcgi

      UseCanonicalName On
      <Directory /home/ffm/www>
        DirectoryIndex index.html
        Order allow,deny
        Allow from all
      </Directory>
    </VirtualHost>


  ### Create a database
  $ python active/www/app/deploy.py create

  ### Put some data into the database

  ### Test deployment script and generate some needed files
    ### Update source code
    $ python passive/www/app/deploy.py update

    ### Compile translations
    $ python passive/www/app/deploy.py babel compile

    ### Byte compile python files
    $ python passive/www/app/deploy.py pycompile

    ### Migrate database from active to passive
    $ python passive/www/app/deploy.py migrate

    ### Setup app cache
    $ python passive/www/app/deploy.py setup_cache

  ### Switch active and passive branches
  $ python passive/www/app/deploy.py switch

Contact
-------

Christian Tanzer <tanzer@swing.co.at>
