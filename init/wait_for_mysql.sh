#!/bin/sh
# Returns true once mysql can connect.
mysql_ready() {
    mysqladmin ping --host=${MYSQL_DATABASE_HOST} --user=${MYSQL_DATABASE_USER} --password=${MYSQL_DATABASE_PASSWORD} --connect-timeout=3 > /dev/null 2>&1
    ret=$?
    return $ret
}

mysql_db_ready() {
    ret=$(mysql --host=${MYSQL_DATABASE_HOST} --user=${MYSQL_DATABASE_USER} --password=${MYSQL_DATABASE_PASSWORD} -s -N \
      -e "select COUNT(*) from information_schema.schemata where schema_name='${MYSQL_DATABASE}';")
    if [ $ret -eq 0 ]
    then
        return 1
    fi
    return 0
}

while !(mysql_ready)
do
    sleep 3
    echo "waiting for mysql ..."
done

while !(mysql_db_ready)
do
    sleep 3
    echo "waiting for database ..."
done