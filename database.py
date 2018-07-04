import dataset

#db = dataset.connect('sqlite:///database.db')
db = dataset.connect('mysql://root:123@localhost/mas_db')
# banco sqlite3 -> local
#db = dataset.connect('sqlite:///database.db')

# banco mysql
#db = dataset.connect('mysql://user:password@localhost/mydatabase')
