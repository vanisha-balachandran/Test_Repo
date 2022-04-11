from flask import Flask, jsonify, request, abort
import project_test1

app = Flask(__name__)
app.config.from_object(__name__)


# error handling
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

#using POST request to add data to DB
@app.route('/projectpost', methods=['POST'])
def post_eg():
    row = project_test1.City_table.create(**request.json)
    query = project_test1.City_table.select().where(
        project_test1.City_table.name == row.name,
        project_test1.City_table.district == row.district
    )
    data = [i.serialize for i in query]
    res = jsonify({
        'city': data,
        'meta': {'page_url': request.url}
    })
    res.status_code = 201
    return res

#using GET & PUT Request to get all data from DB
@app.route('/projectput/<string:country_code>/<string:city_name>', methods=['GET','DELETE','PUT'])
def put_eg(country_code, city_name):
    if request.method == 'GET':
        query = project_test1.City_table.select().where(
            project_test1.City_table.countrycode == country_code,
            project_test1.City_table.name == city_name
        )

        data = [i.serialize for i in query]

        if data:
            res = jsonify({
                'cities': data,
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

    elif request.method == "PUT":  # put endpoint

       c = project_test1.City_table.get(
            project_test1.City_table.countrycode == country_code,
            project_test1.City_table.name == city_name
        )

       if not c:
            abort(404)
       if not request.json:
            abort(400)

       if 'district' in request.json and type(request.json['district']) != str:
            abort(400)
       else:
            c.district = request.json['district']
       if 'population' in request.json and type(request.json['population']) is not int:
            abort(400)
       else:
            c.population = request.json['population']

       c.save()

       query = project_test1.City_table.select().where(
            project_test1.City_table.name == c.name,
            project_test1.City_table.countrycode == c.countrycode
        )
       data = [i.serialize for i in query]
       res = jsonify({
            'city': data,
            'meta': {'page_url': request.url}
        })
       res.status_code = 200
       return res

    elif request.method == "DELETE":  # delete endpoint

        try:
            city = project_test1.City_table.get(
                project_test1.City_table.countrycode == country_code,
                project_test1.City_table.name == city_name
            )
        except:
            city = None

        if city:
            city.delete_instance()
            res = jsonify({"Success": "Item Deleted"})
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