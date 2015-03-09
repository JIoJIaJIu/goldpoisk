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
    for i, image in enumerate(images):
        id = image[2]
        blob = image[1]

        hash = md5(blob).hexdigest()
        keychain.append(hash)

        src = 'product/%s.jpg' % hash
        print '> %d > %s' % (id, src)
        f = open(src, 'w+')
        f.write(image[1])
        sql = 'UPDATE goldpoisk_entity_images set src="%s" where id=%d;' % (src, id)
        cursor.execute(sql)
        f.close()
    con.commit()


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
    save_images(cursor, con)
    cursor.close()
