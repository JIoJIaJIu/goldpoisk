#!/bin/bash
ssh webfaction "
cd goldpoisk

mkdir -p arhives
mv myproject arhives/myproject.${BUILD_NUMBER}

echo 'Stopping uwsgi..'
uwsgi = $(ps -ef | grep [w]sgi | awk '{print $2}')

echo 'processes' $uwsgi
if [ -n $uwsgi ];then
    kill $(ps -ef | grep [w]sgi | awk '{print $2}')
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

rm backend.zip
echo 'Restart uwsgi && nginx..'
uwsgi --master ~/golpoisk/myproject/production.ini
./nginx/sbin/nginx -s reload
"
