README for the FFM web app
===========================

:Authors:

    Christian Tanzer
    <tanzer@swing.co.at>

    Ralf Schlatterbeck
    <rsc@runtux.com>

.. |--| unicode:: U+2013   .. en dash
.. |---| unicode:: U+2014   .. em dash

The FFM web app is an application that serves data about the network
nodes deployed by www.funkfeuer.at.

It uses the `tapyr framework`_.

.. _`tapyr framework`: https://github.com/Tapyr/tapyr

Object model
------------

This object model (in SVG format) is automagically rendered using
`graph.py`_, the result of the last run is kept under version control
(so you can see our progress) in `nodedb.svg`_.

.. _`nodedb.svg`: https://github.com/FFM/FFM/blob/master/doc/nodedb.svg
.. _`graph.py`: https://github.com/FFM/FFM/blob/master/_FFM/graph.py

.. image:: https://raw.github.com/FFM/FFM/master/doc/nodedb.png
    :alt: Object model SVG
    :target: https://github.com/FFM/FFM/blob/master/doc/nodedb.svg

Some notes on the object model: We try to keep only the relevant
attributes of a real-world object in the object itself |---| everything
else is modelled as a relation. The blue arrows denote inheritance
relationships ("IS_A"). The yellow arrows are attributes, e.g., the Node
has an attribute ``manager`` of type ``Person`` which is required (this
is implemented as a foreign key in the database).

The black arrows are 1:N relationships (also implemented as foreign keys
in the database) but the relation objects have their own identity. This
is used to separate the attribute of an object from its links to other
objects. It also implements referential integrity constraints: A link is
deleted if the object to which it points is deleted.

There are different link attributes. A two-way link (implementing an N:M
relationship) has a ``left`` and a ``right`` side which are also the
default attribute names. An example is
``Wireless_Interface_uses_Wireless_Channel``, in the diagram this link
object is displayed as ``_uses_`` between the ``FFM.Wireless_Channel``
and ``FFM.Wireless_Interface``. The black arrows connecting these are
labelled ``left`` and ``right`` which indicates how this should be read.
Note that in this case the ``left`` attribute is on the right side in
the diagram. A two-way link like this has an identity and can have
additional attributes besides ``left`` and ``right``.

There are also unary links with only a ``left`` side. An example is the
``Device`` which cannot exist without its ``left`` attribute, the
``Device_Type``. There can be several devices with the same device type.
This relationship is inherited by ``Antenna`` and ``Antenna_Type`` and
``Net_Device`` and ``Net_Device_Type``.


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

  * `BeautifulSoup`_

  * `python-dateutil`_

  * `docutils`_

  * `flup`_

  * `jinja2`_

  * `plumbum`_

  * `psycopg2`_ or the `mysql package`_ needed by `sqlalchemy`_

  * `pyquery`_

  * `pytz`_

  * `py-bcrypt`_

  * `rcssmin`_, `rjsmin`_ (for minimization of CSS and Javascript files)

  * `rsclib`_

  * `sqlalchemy`_

  * `werkzeug`_

  Most packages are available via the `Python Package Index`_

.. _`Babel`:           http://babel.edgewall.org/
.. _`BeautifulSoup`:   http://www.crummy.com/software/BeautifulSoup/
.. _`python-dateutil`: http://labix.org/python-dateutil
.. _`docutils`:        http://docutils.sourceforge.net/
.. _`flup`:            http://trac.saddi.com/flup
.. _`jinja2`:          http://jinja.pocoo.org/
.. _`plumbum`:         http://plumbum.readthedocs.org/en/latest/index.html
.. _`psycopg2`:        http://packages.python.org/psycopg2/
.. _`mysql package`:   http://mysql-python.sourceforge.net/
.. _`pyquery`:         http://github.com/gawel/pyquery/
.. _`pytz`:            http://pytz.sourceforge.net/
.. _`py-bcrypt`:       http://www.mindrot.org/projects/py-bcrypt/
.. _`rcssmin`:         http://opensource.perlig.de/rcssmin/
.. _`rjsmin`:          http://opensource.perlig.de/rjsmin/
.. _`rsclib`:          http://rsclib.sourceforge.net/
.. _`sqlalchemy`:      http://www.sqlalchemy.org/
.. _`werkzeug`:        http://werkzeug.pocoo.org/
.. _`Python Package Index`: http://pypi.python.org/pypi

Package Installation for Debian Stable aka Squeeze
--------------------------------------------------

The following is an example installation on Debian Stable. It contains
some information that is applicable to other distributions but is quite
Debian-specific in other parts.

If you are running in a virtual machine, you need at least 384 MB of
RAM, 256 MB isn't enough.

Some of the needed Packages are either not in Debian or are too old to
be useful. The following packages can be installed via the Debian
installer::

 apt-get install git libapache2-mod-fcgid postgresql python-pip \
     python-virtualenv python-distribute build-essentials python-pybabel \
     python-dateutil python-docutils python-flup python-jinja2 \
     python-psycopg2 python-dev apache2-mpm-worker

Other packages can be installed using ``pip`` |---| note that you may want
to install some of these into a virtual python environment (virtualenv),
see later in sectioni `How to install`_ |---| depending on your
estimate how often you want to change external packages::

 pip install Babel plumbum pytz rcssmin rjsmin rsclib sqlalchemy \
     werkzeug py-bcrypt python-openssl pyasn1 pyspkac

Create user and database user permitted to create databases::

 adduser ffm
 createuser -d ffm -P

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

Depending on the packages you have already installed system-wide, you
may want to install some packages into the virtual environment if you
anticipate that these will change::

  ### install Python packages into the virtualenv
  ### if one of these packages is already installed in the system
  ### Python, you'll need to say `pip install --upgrade`, not `pip install`
  $ source PVE/active/bin/activate
  $ pip install Babel plumbum pytz werkzeug

Then we continue with the setup of an active and a passive branch of the
web application. With this you can upgrade the passive application while
the active application is running without risking a non-functional
system should something go wrong during the upgrade::

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
  $ git clone git://github.com/Tapyr/tapyr.git v/1/lib
  $ git clone git://github.com/FFM/FFM.git     v/1/www/app
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

Then we configure an Apache virtual host, for instance::

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

To configure Apache to always use https, use something like::

    <VirtualHost *:80>
      ServerName   xxx.funkfeuer.at
      RewriteEngine On
      RewriteRule ^/(.*)$ https://xxx.funkfeuer.at/$1 [L,R]
      RewriteRule ^$ https://xxx.funkfeuer.at [L,R]
    </VirtualHost>

    <VirtualHost *:443>
      ServerName   xxx.funkfeuer.at
      DocumentRoot /home/ffm/active/www

      SSLEngine on
      SSLCertificateFile    /etc/ssl/certs/xxx.pem
      SSLCertificateKeyFile /etc/ssl/private/xxx.key
      SSLCipherSuite HIGH
      SSLProtocol all -SSLv2

      AddDefaultCharset utf-8
      ### as above for the http case
    </VirtualHost>

For Debian the apache configuration should be placed into
``/etc/apache2/sites-available/``, e.g., into the file
``nodedb2.example.com`` and enabled. You probably will have to disable
the default site installed. We used the following commands |---| we
also enable some needed modules::

  a2ensite nodedb2.example.com
  a2dissite default
  a2enmod mod_expires
  a2enmod fcgid
  /etc/init.d/apache2 restart

For https sites, you'll also need the modules::

  a2enmod rewrite
  a2enmod ssl

Finally we create a database and populate it with data::

  ### Create a database
  $ python active/www/app/deploy.py create

  ### Put some data into the database

Whenever we need to upgrade the installation, we can update the passive
configuration, set up everything, migrate the data from the active to
the passive configuration, and if everything went OK, enable it by
exchanging the symbolic links to the active and passive configuration::

  ### Test deployment script and generate some needed files
    ### Update source code
    $ python passive/www/app/deploy.py update

    ### Byte compile python files
    $ python passive/www/app/deploy.py pycompile

    ### Compile translations
    $ python passive/www/app/deploy.py babel compile

    ### Migrate database from active to passive
    $ python passive/www/app/deploy.py migrate -A -P

    ### Setup app cache
    $ python passive/www/app/deploy.py setup_cache

  ### Switch active and passive branches
  $ python passive/www/app/deploy.py switch

Contact
-------

Christian Tanzer <tanzer@swing.co.at> and
Ralf Schlatterbeck <rsc@runtux.com>
