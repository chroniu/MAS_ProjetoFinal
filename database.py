import dataset

# banco sqlite3 -> local
#db = dataset.connect('sqlite:///database.db')

# banco mysql
db = dataset.connect('mysql://user:password@localhost/mydatabase')
