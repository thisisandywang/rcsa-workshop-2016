#!/bin/bash
if [ -z "$1" ]
    then echo 'You must provide a numeric argument, different than existing run config numbers'
else
    cd ~/new_rcsa/
    git pull origin master
    cd ~/public_html
    cp run.fcgi run_$1.fcgi
    cp .htaccess_template .htaccess
    echo 'RewriteRule ^(.*)$ /run'$1'.fcgi/$1 [QSA,L]' >> .htaccess
fi
