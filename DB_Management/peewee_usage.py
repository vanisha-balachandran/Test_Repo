from psycopg2 import connect,extensions,sql


DB_NAME = "database_test1"

conn = connect(host='localhost', user='postgres', password='srisai@2005')

# get the isolation leve for autocommit
autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
print("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)

# set the isolation level for the connection's cursors
# will raise ActiveSqlTransaction exception otherwise
conn.set_isolation_level(autocommit)

cursor = conn.cursor()
cursor.execute('CREATE DATABASE ' + str(DB_NAME))
conn.close()
