#!/usr/bin/python3

import sqlite3

db_filename = 'threads.db'
newline_indent = '\n   '

db=sqlite3.connect(db_filename)
db.text_factory = str
cur = db.cursor()

result = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
table_names = sorted(list(zip(*result))[0])
print ("\ntables are:"+newline_indent+newline_indent.join(table_names))

for table_name in table_names:
    result = cur.execute("PRAGMA table_info('%s')" % table_name).fetchall()
    column_names = list(zip(*result))[1]
    print (("\ncolumn names for %s:" % table_name)
           +newline_indent
           +(newline_indent.join(column_names)))

db.close()
print ("\nexiting.")
