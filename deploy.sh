#!/bin/bash
export PYTHONPATH=/home/guro/goldpoisk/myproject:/home/guro/goldpoisk/lib/python2.7:/home/guro/lib/python2.7/:$PYTHONPATH
cd goldpoisk
echo "We are here" `pwd`

mkdir -p arhives;
mv myproject arhives/myproject.${BUILD_NUMBER}

echo 'Stopping u[w]sgi..';
pr=$(ps -ef | grep [w]sgi | awk '{print $2}')
if [ -n "$pr" ];then
    echo 'processes' $pr
    kill $pr
    sleep 1
fi

echo 'Unzipping project..'
unzip -o backend.zip -d myproject
mv myproject/goldpoisk/settings.prod.py myproject/goldpoisk/settings.py
sleep 1

echo 'Copy third-parties..'
cp -rv arhives/myproject.${BUILD_NUMBER}/static/js/third-parties myproject/static

echo 'Migrations..'
echo 'Copy migration goldpoisk'
cp -r arhives/myproject.${BUILD_NUMBER}/goldpoisk/migrations myproject/goldpoisk/
echo 'Copy migration product..'
cp -r arhives/myproject.${BUILD_NUMBER}/goldpoisk/product/migrations myproject/goldpoisk/product/
echo 'Copy migration shop'
cp -r arhives/myproject.${BUILD_NUMBER}/goldpoisk/shop/migrations myproject/goldpoisk/shop/
sleep 1

rm backend.zip
echo 'Restart uwsgi && nginx..'
~/bin/uwsgi --master ~/goldpoisk/myproject/production.ini &
./nginx/sbin/nginx -s reload
