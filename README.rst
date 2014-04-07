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

  * `docutils`_

  * `flup`_

  * `jinja2`_

  * `m2crypto`_

  * `passlib`_

  * `plumbum`_

  * `psycopg2`_

  * `py-bcrypt`_

  * `pyOpenSSL`_

  * `pyasn1`_

  * `pyquery`_

  * `python-dateutil`_

  * `pytz`_

  * `rcssmin`_, `rjsmin`_ (for minimization of CSS and Javascript files)

  * `rsclib`_

  * `sqlalchemy`_

  * `werkzeug`_

  Most packages are available via the `Python Package Index`_

.. _`Babel`:           http://babel.edgewall.org/
.. _`BeautifulSoup`:   http://www.crummy.com/software/BeautifulSoup/
.. _`Python Package Index`: http://pypi.python.org/pypi
.. _`docutils`:        http://docutils.sourceforge.net/
.. _`flup`:            http://trac.saddi.com/flup
.. _`jinja2`:          http://jinja.pocoo.org/
.. _`m2crypto`:        http://pypi.python.org/pypi/M2Crypto
.. _`passlib`:         http://code.google.com/p/passlib/
.. _`plumbum`:         http://plumbum.readthedocs.org/en/latest/index.html
.. _`psycopg2`:        http://packages.python.org/psycopg2/
.. _`py-bcrypt`:       http://code.google.com/p/py-bcrypt/
.. _`pyOpenSSL`:       https://launchpad.net/pyopenssl
.. _`pyasn1`:          http://pyasn1.sourceforge.net/
.. _`pyquery`:         http://github.com/gawel/pyquery/
.. _`python-dateutil`: http://labix.org/python-dateutil
.. _`pytz`:            http://pytz.sourceforge.net/
.. _`rcssmin`:         http://opensource.perlig.de/rcssmin/
.. _`rjsmin`:          http://opensource.perlig.de/rjsmin/
.. _`rsclib`:          http://rsclib.sourceforge.net/
.. _`sqlalchemy`:      http://www.sqlalchemy.org/
.. _`werkzeug`:        http://werkzeug.pocoo.org/

Package Installation for Debian Stable aka Wheezy
--------------------------------------------------

The following is an example installation on Debian Wheezy. It contains
some information that is applicable to other distributions but is quite
Debian-specific in other parts.

If you are running in a virtual machine, you need at least 384 MB of
RAM, 256 MB isn't enough.

Some of the needed Packages are either not in Debian or are too old to
be useful. The following packages can be installed via the Debian
installer::

 $ apt-get install \
     apache2-mpm-worker build-essential git libapache2-mod-fcgid \
     postgresql python-pip python-babel python-bs4 python-dateutil \
     python-dev python-distribute python-docutils python-flup \
     python-jinja2 python-m2crypto python-openssl python-passlib \
     python-psycopg2 python-pyasn1 python-pyquery python-sqlalchemy \
     python-tz python-virtualenv python-werkzeug swig

Other packages can be installed using ``pip`` |---| note that you may want
to install some of these into a virtual python environment (virtualenv),
see later in sectioni `How to install`_ |---| depending on your
estimate how often you want to change external packages::

 $ pip install plumbum py-bcrypt rcssmin rjsmin rsclib pyspkac

Create user and database user permitted to create databases::

 $ adduser ffm
 $ createuser -d ffm -P

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
  $ python -m virtualenv --system-site-packages PVE/std
  $ (cd PVE ; ln -s std active)

Depending on the packages you have already installed system-wide, you
may want to install some packages into the virtual environment if you
anticipate that these will change::

  ### install Python packages into the virtualenv
  ### if one of these packages is already installed in the system
  ### Python, you'll need to say `pip install --upgrade`, not `pip install`
  $ source PVE/active/bin/activate
  $ pip install plumbum pytz py-bcrypt rcssmin rjsmin rsclib pyspkac

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

With a small config-file, the deploy-app can automatically create an
Apache configuration file and a fcgi script. You can find sample
config-files in active/www/app/httpd_config/. For instance,
active/www/app/httpd_config/ffm_gg32_com__443.config contains::

        config_path     = "~/fcgi/ffm_gg32_com__443.config"
        host_macro      = "gtw_host_ssl"
        port            = "443"
        script_path     = "~/fcgi/ffm_gg32_com__443.fcgi"
        server_admin    = "christian.tanzer@gmail.com"
        server_name     = "ffm.gg32.com"
        ssl_key_name    = "srvr1-gg32-com-2048"

Create a config::

  ### Create a fcgi script and config for Apache
  $ python active/www/app/deploy.py create_config \
      -HTTP_Config <your-config> -input_encoding=utf-8

You can use the created Apache configuration as is, or modify it
manually or by modifiying the template.

For Debian, the apache configuration should be placed into
``/etc/apache2/sites-available/``, e.g., into the file
``nodedb2.example.com``, and enabled. You probably will have to disable
the default site installed. We used the following commands |---| we
also enable some needed modules::

  $ a2ensite nodedb2.example.com
  $ a2dissite default
  $ a2enmod mod_expires
  $ a2enmod fcgid
  $ /etc/init.d/apache2 restart

For https sites, you'll also need the modules::

  $ a2enmod rewrite
  $ a2enmod ssl

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
    $ python passive/www/app/deploy.py migrate -Active -Passive -verbose

    ### Setup app cache
    $ python passive/www/app/deploy.py setup_cache

  ### Switch active and passive branches
  $ python passive/www/app/deploy.py switch
  $ sudo /etc/init.d/apache2 restart

Contact
-------

Christian Tanzer <tanzer@swing.co.at> and
Ralf Schlatterbeck <rsc@runtux.com>
