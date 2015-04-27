import os
import shutil

import MySQLdb as mdb
from md5 import md5
from _mysql_exceptions import OperationalError

USER_NAME = 'dev_goldpoisk'
USER_PASSWORD = 'dev12345'
DATABASE = 'goldpoisk_dump'

def connect ():
    con = mdb.connect('localhost', USER_NAME, USER_PASSWORD, DATABASE)
    print 'Was opened connection'
    return con

def save_images (cursor, con):
    cursor.execute('SELECT * from goldpoisk_entity_images')
    keychain = []
    images = cursor.fetchall()
    desc = [d[0].decode('utf-8') for d in cursor.description]
    if os.path.exists('product'):
        shutil.rmtree('product')
    os.mkdir('product')

    for i, image in enumerate(images):
        id = image[desc.index('id')]
        blob = image[desc.index('image')]

        hash = md5(blob).hexdigest()
        keychain.append(hash)

        src = 'product/%s.jpg' % hash
        print '> %d > %s' % (id, src)
        f = open(src, 'w+')
        f.write(blob)
        sql = 'UPDATE goldpoisk_entity_images set src="%s" where id=%d;' % (src, id)
        cursor.execute(sql)
        f.close()
    con.commit()


def alter_table (cursor):
    try:
        cursor.execute('SELECT id from goldpoisk_entity_images')
    except OperationalError as e:
        cursor.execute('ALTER TABLE goldpoisk_entity_images ADD id INT AUTO_INCREMENT UNIQUE');
        print 'Successuful adding `id` to table'

    try:
        cursor.execute('SELECT src from goldpoisk_entity_images')
    except OperationalError as e:
        cursor.execute('ALTER TABLE goldpoisk_entity_images ADD src CHAR(128)');
        print 'Successuful adding `src` to table'

if __name__ == '__main__':
    con = connect()
    cursor = con.cursor()

    alter_table(cursor)
    save_images(cursor, con)
    cursor.close()
