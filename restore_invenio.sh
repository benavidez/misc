#!/bin/bash
echo "*****************************"
function restore_invenio {
    echo "*** restoring invenio dir"
    rm -rf /opt/invenio
    cp -r /opt/invenio.bk /opt/invenio
}

function restore_db {
    echo "*** restoring invenio db"
    /sbin/service mysqld restart
    mysql -uroot -p invenio < /opt/bk/invenio.9.6.dmp
}

function update_all {
    echo "*** updating all and restarting apache"
    chown apache:apache -R /opt/invenio
    chmod 775 -R /opt/invenio

    /opt/invenio/bin/inveniocfg --update-all && /sbin/service httpd restart
}

#********** MAIN ******************
restore_invenio
restore_db
update_all

echo Done
