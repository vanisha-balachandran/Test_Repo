from flask import Flask, request, jsonify
from peewee import *

app = Flask(__name__)

@app.route('/todolist')
def todo():
    return jsonify({"Msg": "Test Project Sai"})



#create a database using PostgerSQL
db = PostgresqlDatabase('database_test1', host='localhost', port=5432, user='postgres', password='srisai@2005')

class table_Eg(Model):
   name=TextField()
   city=TextField()
   age=TextField()
   class Meta:
      database=db
      db_table='table_Eg'

db.connect()
db.create_tables([table_Eg])

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
        table_Eg.create(**data_dict)

#using POST request
@app.route('/todolist2', methods=['POST'])
def post_eg():
    row = table_Eg.create(**request.json)
    query = table_Eg.select().where(
        table_Eg.name == row.name,
        table_Eg.city == row.city,
        table_Eg.age == row.age,
    )
    #data = [i.serialize for i in query]
    data = {
        'name': str(row.name),
        'city': str(row.city),
        'age': str(row.age)
    }
    res = jsonify({
        'data_dict': data,
        })
    res.status_code = 201
    return res

#using GET method - importing all data
@app.route('/todolist1', methods=['GET'])
def get_eg():
    query_val = table_Eg.select()
    num_data = list(query_val)
    data = {
        'name': str(table_Eg.name).strip(),
        'city': str(table_Eg.city).strip(),
        'age': str(table_Eg.age).strip()
    }
    if data:
    #data = [i.serialize for i in query]

        res = jsonify({
            'data_dict': data,
            'meta': {'page_url': request.url}
        })
        res.status_code = 200
    else:
        output = {
            "error": "No results found. Check url again",
            "url": request.url,
        }
        res = jsonify(output)
        res.status_code = 404
    return res

#using GET operation and one particular id
@app.route('/todolist1/<string:name>', methods=['GET'])
def city_country_endpoint(name):

    # get request
    if request.method == 'GET':
        query = table_Eg.select().where(table_Eg.name == name)
        data = {
            'name': str(table_Eg.name).strip(),
            'city': str(table_Eg.city).strip(),
            'age': str(table_Eg.age).strip()

        }

        if data:
            res = jsonify({
                'dict': data,
                'meta': {'page_url': request.url}
                })
            res.status_code = 200
        else:
            output = {
                "error": "No results found. Check url again",
                "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res

#using DELETE opration to delete a instance from db
@app.route('/todolist_delete',methods=["DELETE"])
def delete_oper(name):
    try:
        delete_name = table_Eg.get(table_Eg.name == name)
    except:
        delete_name = None
    if delete_name:
        delete_name.deleteinstance()
        res = jsonify({})
        res.status_code = 204
        return res
    else:
        res = jsonify({
            "Error": "The requested resource is no longer available at the "
                     "server and no forwarding address is known.",
            "Status Code": 410,
            "URL": request.url
        })
        res.status_code = 410
        return res

if __name__ == "__main__":
    app.run(debug=True)