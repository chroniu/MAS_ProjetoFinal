#import pymysql
#pymysql.install_as_MySQLdb()
import MySQLdb
    #import dataset
    #db = dataset.connect('sqlite:///database.db')
    #db = dataset.connect('mysql://root:123@localhost/mas_db')

db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123', db='mas_db')
#db.select_db('mas_db')
