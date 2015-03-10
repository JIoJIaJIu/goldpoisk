#!/bin/bash
cd goldpoisk/myproject

echo 'Unzipping frontend..'
unzip -o frontend.zip -d frontend/index
if [ $? -ne 0 ]; then
    exit 1
fi;

rm frontend.zip

echo 'Restarting uwsgi..'
kill $(ps -ef | grep [w]sgi | awk '{print $2}')
sleep 1;
uwsgi --master ~/golpoisk/myproject/production.ini &

if [$? -ne 0]; then
    exit 1
fi;

echo 'Unzipping static..'
unzip -o frontend.static.zip -d static
cp frontend/index/index.bemhtml.js static/
cp frontend/index/index.priv static/

if [ $? -ne 0 ]; then
    exit 1
fi;

rm frontend.static.zip
