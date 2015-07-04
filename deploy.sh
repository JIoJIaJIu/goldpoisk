#!/bin/bash
export PYTHONPATH=/home/guro/goldpoisk/myproject:/home/guro/goldpoisk/lib/python2.7:/home/guro/lib/python2.7/:$PYTHONPATH

restart_server() {
    echo 'Stopping u[w]sgi..'
    pr=$(ps -ef | grep [w]sgi | awk '{print $2}')
    if [ -n "$pr" ]; then
        echo 'processes' $pr
        kill $pr
        sleep 1
    fi

    echo 'Starting uwsgi..'
    cd ~/goldpoisk
    ~/bin/uwsgi ~/goldpoisk/myproject/production.ini --reload-on-rss 500 &

    echo 'Restarting nginx..'
    ./nginx/sbin/nginx -s reload
}

copy_backend_static() {
    cd ~/goldpoisk
    echo 'Generate sitemap.xml'
    python myproject/utils/sitemap.py
    mv -v sitemap.xml static/

    echo 'Collect static'
    python manage.py collectstatic --noinput
}

copy_migrations() {
    echo 'Migrations..'
    echo 'Copy migration goldpoisk'
    cp -r arhives/myproject.${BUILD_NUMBER}/goldpoisk/migrations myproject/goldpoisk/
    echo 'Copy migration product..'
    cp -r arhives/myproject.${BUILD_NUMBER}/goldpoisk/product/migrations myproject/goldpoisk/product/
    echo 'Copy migration shop'
    cp -r arhives/myproject.${BUILD_NUMBER}/goldpoisk/shop/migrations myproject/goldpoisk/shop/
    echo 'Copy migration cms'
    cp -r arhives/myproject.${BUILD_NUMBER}/goldpoisk/cms/migrations myproject/goldpoisk/cms/
    sleep 1
}

unzip_backend() {
    mkdir -p arhives;
    mv myproject arhives/myproject.${BUILD_NUMBER}

    echo 'Unzipping backend..'
    unzip -o backend.zip -d myproject
    mv myproject/goldpoisk/settings.prod.py myproject/goldpoisk/settings.py
    rm backend.zip
    sleep 1
}

unzip_frontend() {
    cd ~/goldpoisk
    echo 'Unzipping frontend..'
    rm -rf myproject/frontend/index
    unzip -o frontend.zip -d myproject/frontend/index
    rm frontend.zip
    sleep 1
}

copy_frontend_static() {
    cd ~/goldpoisk
    echo 'Unzipping static..'
    unzip -o frontend.static.zip -d static
    cp myproject/frontend/index/index.bemhtml.js static/js/
    cp myproject/frontend/index/index.priv.js static/js/

    if [ $? -ne 0 ]; then
        exit 1
    fi;

    rm frontend.static.zip
}

usage() {
    echo 'Deploy system for goldpoisk'
    echo '  --backend - deploy backend'
    echo '  --frontend - deploy frontend'
}

for i in $@; do
    case $i in
       --backend)
           unzip_backend
           copy_backend_static
           copy_migrations
           restart_server
           exit 0
           ;;
       --frontend)
           unzip_frontend
           copy_frontend_static
           restart_server
           exit 0
           ;;
    esac
done;

usage
