#from psycopg2 import connect,extensions,sql
from peewee import *

db = PostgresqlDatabase('database_test1', host='localhost', port=5432, user='postgres', password='srisai@2005')

class MyUser (Model):
   name=TextField()
   city=TextField(constraints=[SQL("DEFAULT 'Mumbai'")])
   age=IntegerField()
   class Meta:
      database=db
      db_table='MyUser1'

db.connect()
db.create_tables([MyUser1])

#Add
rec1=MyUser1.insert(name="Rajesh", age=21)
rec1.save()