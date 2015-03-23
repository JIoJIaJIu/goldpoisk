#!/bin/sh

DB_USER='dev_goldpoisk'
DB_NAME='goldpoisk_dump'
DB_PASSWORD='dev12345'

MYSQL="mysql -h localhost -u $DB_USER -p$DB_PASSWORD $DB_NAME"

function show_help {
    echo "Usage:"
    echo "-a|--add file: add dump"
    echo "-c|--clean: clean goldpoisk_dump database"
}

TABLES="goldpoisk_entity
        goldpoisk_entity_images
        goldpoisk_kamni"

for i in $@; do
    case $i in
        -a|--add)
            echo "Adding dump"
            set -x
            $MYSQL < $2
            set +x
            T=`$MYSQL -e "show tables"`;
            for i in $T; do
                echo $i
                $MYSQL -e "describe $i"
            done
            ;;
        -c|--clean)
            set -x
            $MYSQL -vvv -e "drop table if exists `echo $TABLES|tr ' ' ','`"
            set +x
            ;;
        -h|--help)
            show_help
            ;;
        *)
            ;;
    esac
done
