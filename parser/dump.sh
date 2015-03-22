#!/bin/sh

DB_NAME=dev_goldpoisk
DB_USER=dev_goldpoisk
DB_HOST=localhost

function show_help {
    echo "Usage.."
    echo "-c|--create create dump"
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
        product_image \
        shop_shop \
        shop_admin \
        shop_manager"

function concat {
    for i in $@; do
        RES+="|"+$i
    done
}

function export_dump {
    echo "Creating dump.."

    set -o xtrace
    $PGDUMP --schema=public --table="(`echo $TABLES | tr ' ' '|'`)" > dump.sql
    set +o xtrace
}

DUMP=dump.sql

function upload_dump {
    echo "Upload dump.."
    set -o xtrace
    $PSQL -c "DROP TABLE `echo $TABLES | tr ' ' ','`"
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
