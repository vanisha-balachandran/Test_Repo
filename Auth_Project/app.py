from flask import Flask, jsonify, request, abort, g
from flask_httpauth import HTTPBasicAuth
import model
import os

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = "c21f347994c74b0daa22f37d593427d8"
auth = HTTPBasicAuth()


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


# Authentication callback
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = model.UserData.verify_auth_token(username_or_token)
    if not user:
        # Second try to authenticate by login credentials
        user = model.UserData.get(model.UserData.username == username_or_token)
        if not user or not user.verify_password(password):
            return False
        g.user = user
    return True


# token endpoint
@app.route('/api/v1/token')
@auth.login_required
def get_auth_token():
    duration = 600
    token = g.user.generate_auth_token(duration)
    return jsonify({
        'token': token.decode('ascii'),
        'duration': duration,
        'message': 'After Duration: {duration} secs, request for a new token.'.format(duration=duration)
     })


# User registration
@app.route('/api/v1/users', methods=['POST'])
def add_new_user():
    username = request.json['username']
    password = request.json['password_hash']


    if username is None or password is None:
        abort(400)
    try:
        user = model.UserData.get(model.UserData.username == username)
    except:
        user = None

    if user is not None:
        abort(400)

    user = model.UserData(username=username, password_hash=password)
    user.hash_password()
    user.save()
    res = jsonify({'username': user.username, "meta": {"page_url": request.url}})
    res.status_code = 201
    return res

#using POST request to add data to DB
@app.route('/projectpost', methods=['POST'])
def post_eg():
    row = model.City.create(**request.json)
    query = model.City.select().where(
        model.City.name == row.name,
        model.City.district == row.district
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
        query = model.City.select().where(
            model.City.countrycode == country_code,
            model.City.name == city_name
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

       c = model.City.get(
            model.City.countrycode == country_code,
            model.City.name == city_name
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

       query = model.City.select().where(
            model.City.name == c.name,
            model.City.countrycode == c.countrycode
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
            city = model.City.get(
                model.City.countrycode == country_code,
                model.City.name == city_name
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