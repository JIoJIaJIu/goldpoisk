#!/bin/bash
ssh webfaction "
cd goldpoisk

mkdir -p arhives
mv myproject arhives/myproject.${BUILD_NUMBER}

echo 'Stopping uwsgi..'
kill $(ps -ef | grep [w]sgi | awk '{print $2}')

echo 'Unzipping project..'
unzip -o backend.zip -d myproject
mv myproject/goldpoisk/settings.prod.py myproject/goldpoisk/settings.py

echo 'Migrations..'
echo 'Migration product..'
cp -r arhives/myproject.${BUILD_NUMBER}/goldpoisk/product/migrations myproject/goldpoisk/product/
python manage.py makemigrations product -v 2
python manage.py migrate product -v 2

rm backend.zip
echo 'Restart uwsgi && nginx..'
uwsgi --master ~/golpoisk/myproject/production.ini
./nginx/sbin/nginx -s reload
"
