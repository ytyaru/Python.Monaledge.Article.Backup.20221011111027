import sqlite3
con = sqlite3.connect(':memory:')
cur = con.cursor()
for row in cur.execute("select 'Hello SQLite3 !!';"):
	print(row[0])
cur.close()
# sqlite3.ProgrammingError: executemany() can only execute DML statements.
#for row in cur.executemany("select ?,?;", [(0, 'yamada')]):
#	print(row)
# 結果が何も表示されない
#for row in cur.executescript("select 0,'yamada'; select 1,'suzuki';"):
#	print(row)

