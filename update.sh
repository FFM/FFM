#!/bin/sh

#terminate on errors
set -e

# In case there are some software updates for the FFM python code, 
# you should execute this

# as root:
#sudo /etc/init.d/apache2 stop

# as user ffm
python passive/www/app/deploy.py update
python passive/www/app/deploy.py pycompile
python passive/www/app/deploy.py migrate -Active -Passive -verbose
python passive/www/app/deploy.py setup_cache
python passive/www/app/deploy.py switch

# as root:
#sudo /etc/init.d/apache2 start
