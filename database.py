import dataset

<<<<<<< HEAD
#db = dataset.connect('sqlite:///database.db')
db = dataset.connect('mysql://root:123@localhost/mas_db')
=======
# banco sqlite3 -> local
#db = dataset.connect('sqlite:///database.db')

# banco mysql
db = dataset.connect('mysql://user:password@localhost/mydatabase')
>>>>>>> a932f43df717f1a8901b4f5fb29afa345cc7681c
