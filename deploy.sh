#!/bin/bash
cd goldpoisk;

mkdir -p arhives;
mv myproject arhives/myproject.${BUILD_NUMBER};

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

echo 'Migrations..'
echo 'Migration product..'
cp -r arhives/myproject.${BUILD_NUMBER}/goldpoisk/product/migrations myproject/goldpoisk/product/
python myproject/manage.py makemigrations product -v 2
python myproject/manage.py migrate product -v 2
sleep 1

rm backend.zip
echo 'Restart uwsgi && nginx..'
uwsgi --master ~/golpoisk/myproject/production.ini
./nginx/sbin/nginx -s reload
