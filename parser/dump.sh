#!/bin/sh

DB_USER=dev_goldpoisk
DB_NAME=dev_goldpoisk
DB_HOST=localhost
DUMP=${2:-dump.sql}

function show_help {
    echo "Usage.."
    echo "-c|--create: create dump"
    echo "-u|--upload file: upload dump to server webfaction:goldpoisk/dumps"
    echo "-a|--add file: add dump"
    echo "-as file: add dump on server to dev and test db"
    echo "-h|--help: show this help"
}

PGRESTORE="pg_restore -h $DB_HOST -v -U $DB_NAME -w -d $DB_NAME"
PGDUMP="pg_dump -h $DB_HOST -v -U $DB_NAME -w -d $DB_NAME"
TABLES="product_product_gems \
        goldpoisk_bestbid \
        goldpoisk_action \
        goldpoisk_hit \
        product_product_materials \
        product_product \
        product_item \
        product_material \
        product_gem \
        product_image"

function export_dump {
    echo "Creating dump.."
    set -o xtrace
    $PGDUMP --schema=public --table="(`echo $TABLES | tr ' ' '|'`)" > $DUMP 
    set +o xtrace
}

function add_dump {
    echo "Adding dump.."
    if [ ! -f $DUMP ]; then
        echo "No dump $2!"
        exit 1
    fi

    USER=${1:-$DB_USER}
    NAME=${2:-$DB_NAME}

    PSQL="psql -h $DB_HOST -v -U $USER -w -d $NAME"
    set -o xtrace
    $PSQL -c "DROP TABLE if exists `echo $TABLES | tr ' ' ','`"
    $PSQL < $DUMP
    set +o xtrace
}

function add_dump_on_server {
    echo "Adding dump to dev and test dbs"
    set -x
    add_dump 
    add_dump dumper copy_goldpoisk
    set +x
}

function upload_dump {
    echo "Uploading dump"
    set -x
    rsync --progress -v $DUMP webfaction:goldpoisk/dumps/${DUMP##*/}
    set +x
}

for i in $@; do
    case $i in
        -c|--create)
            export_dump
            ;;
        -h|--help)
            show_help
            ;;
        -a|--add)
            add_dump
            ;;
        -as)
            add_dump_on_server
            ;;
        -u|--upload)
            upload_dump
            ;;
        *)
            show_help
            ;;
    esac
    exit 0
done
