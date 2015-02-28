import MySQLdb as mdb
from _mysql_exceptions import OperationalError
from PIL import Image

USER_NAME = 'dev_goldpoisk'
USER_PASSWORD = 'dev12345'
DATABASE = 'goldpoisk_dump'

def connect ():
    con = mdb.connect('localhost', USER_NAME, USER_PASSWORD, DATABASE)
    print 'Was opened connection'
    return con

def save_images (cursor):
    cursor.execute('SELECT * from goldpoisk_entity_images')
    images = cursor.fetchmany(10000) #TODO 10000
    image = images[0]
    for i, image in enumerate(images):
        f = open('images/img-%d.jpg' % i, 'w+')
        f.write(image[1])
        f.close()


def alter_table (cursor):
    try:
        cursor.execute('SELECT src from goldpoisk_entity_images')
        print 'Not needed alter table'
    except OperationalError as e:
        cursor.execute('ALTER TABLE goldpoisk_entity_images ADD src CHAR(128)');
        print 'Successuful alter table'

if __name__ == '__main__':
    con = connect()
    cursor = con.cursor()

    alter_table(cursor)
    save_images(cursor)
