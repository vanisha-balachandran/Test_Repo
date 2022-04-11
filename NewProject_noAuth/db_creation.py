from flask import Flask, request, jsonify
from peewee import *

app = Flask(__name__)

@app.route('/todolist')
def todo():
    return jsonify({"Msg": "Test Project Sai"})



#create a database using PostgerSQL
db = PostgresqlDatabase('NewProject_DB', host='localhost', port=5432, user='postgres', password='srisai@2005')

class table_Eg1(Model):
   name=TextField()
   city=TextField()
   age=TextField()
   class Meta:
      database=db
      db_table='table_Eg1'

db.connect()
db.create_tables([table_Eg1])

@property
def serialize(self):
    data = {
        'id': self.id,
        'name': str(self.name).strip(),
        'city': str(self.city).strip(),
        'age': str(self.age).strip()

    }
    return data

def __repr__(self):
    return "{}, {}, {}, {}".format(
        self.id,
        self.name,
        self.city,
        self.age
    )

data_source = [
    {'name': 'name11', 'city': 'city11', 'age': '11'},
    {'name': 'name12', 'city': 'city12', 'age': '21'},
    {'name': 'name13', 'city': 'city13', 'age': '31'},
    {'name': 'name14', 'city': 'city14', 'age': '41'},
    {'name': 'name15', 'city': 'city15', 'age': '51'},
]
#insert bulk data to db
with db.atomic():
    for data_dict in data_source:
        table_Eg1.create(**data_dict)