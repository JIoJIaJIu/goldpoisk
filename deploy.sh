echo "Starting Deploy"

if [ ! -f $1 ]; then
    echo "There is no artifact"
    exit 1
fi

ssh teamcity

cd /home/guro/webapps/goldpoisk
echo "Stoping server"
apache2/bin/stop

echo "Unzip artifact"
unzip $1 -d myproject

echo "Syncdb"
cd myproject
python manage.py syncdb --no-input

echo "Starting server"
../apache2/bin/start
