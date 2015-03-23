#!/bin/sh

DB_NAME=dev_goldpoisk
DB_USER=dev_goldpoisk
DB_HOST=localhost

function show_help {
    echo "Usage.."
    echo "-c|--create create dump"
    echo "-u|--upload upload dump"
    echo "-h|--help show this help"
}

PSQL="psql -h $DB_HOST -v -U $DB_NAME -w -d $DB_NAME"
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
    $PGDUMP --schema=public --table="(`echo $TABLES | tr ' ' '|'`)" > dump.sql
    set +o xtrace
}

DUMP=$2
function upload_dump {
    echo "Upload dump.."
    if [ ! -f $DUMP ]; then
        echo "No dump $2!"
        exit 1
    fi

    set -o xtrace
    $PSQL -c "DROP TABLE if exists `echo $TABLES | tr ' ' ','`"
    $PSQL < $DUMP
    set +o xtrace
}

for i in $@; do
    case $i in
        -c|--create)
            export_dump
            ;;
        -h|--help)
            show_help
            ;;
        -u|--upload)
            upload_dump
            ;;
        *)
            show_help
            ;;
    esac
done
