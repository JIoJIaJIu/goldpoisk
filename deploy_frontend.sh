#!/bin/bash
cd goldpoisk/myproject

echo 'Unzipping frontend..'
unzip -o frontend.zip -d frontend/index
if [ $? -ne 0 ]; then
    exit 1
fi;

rm frontend.zip

echo 'Restarting uwsgi..'
pr=$(ps -ef | grep [w]sgi | awk '{print $2}')
echo $pr
kill -2 $pr
sleep 1;

cd ~/goldpoisk
~/bin/uwsgi ~/goldpoisk/myproject/production.ini &

if [ $? -ne 0 ]; then
    exit 1
fi;

echo 'Unzipping static..'
unzip -o frontend.static.zip -d static
cp frontend/index/index.bemhtml.js static/js/
cp frontend/index/index.priv.js static/js/

if [ $? -ne 0 ]; then
    exit 1
fi;

rm frontend.static.zip
