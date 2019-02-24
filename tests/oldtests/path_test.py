from os import path

CUR_PATH = path.dirname( path.abspath( __file__ ) )
SQLITE_DB_LOC = '../data/database.db'

SQL_ABS_LOC = path.abspath( path.join( CUR_PATH, SQLITE_DB_LOC ) )

print( SQL_ABS_LOC )

<<<<<<< HEAD
# print( path.)
=======
# HOME_PATH = path
# print( HOME_PATH )
print( path.expanduser("~") )
>>>>>>> 7b5dadfc4ace7164a0eb2308a9af98991048dd79
