#!/bin/bash
ssh webfaction "

cd goldpoisk/myproject

echo 'Unzipping static..'
unzip -o frontend.static.zip -d static

if [$? -ne 0]; then
    exit 1
fi;

rm frontend.static.zip

echo 'Unzipping frontend..'
unzip -o frontend.zip -d frontend/index
if [$? -ne 0]; then
    exit 1
fi;

rm frontend.zip

echo 'Restarting uwsgi..'
kill $(ps -ef | grep [w]sgi | awk '{print $2}')
sleep 1;
uwsgi --master ~/golpoisk/myproject/production.ini

if [$? -ne 0]; then
    exit 1
fi;
"
