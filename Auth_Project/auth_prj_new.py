from flask import Flask, request, jsonify, make_response
from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'

psql_db = PostgresqlDatabase(
    'TestDB1',
    user='postgres',
    password='srisai@2005',
    host='localhost',
)


class BaseModel(Model):

    class Meta:
        database = psql_db
        db_table = 'city'
        table_alias = 'c'


class City(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=35)
    countrycode = CharField(max_length=3)
    district = CharField(max_length=20)
    population = BigIntegerField()

    @property
    def serialize(self):
        data = {
            'id': self.id,
            'name': str(self.name).strip(),
            'countrycode': str(self.countrycode).strip(),
            'district': str(self.district).strip(),
            'population': self.population,
        }

        return data

    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(
            self.id,
            self.name,
            self.countrycode,
            self.district,
            self.population
        )


class UserData(Model):
    id = PrimaryKeyField(null=False)
    username = CharField(max_length=50, unique=True)
    password_hash = CharField(max_length=128)

    @property
    def serialize(self):
        data = {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash
        }

        return data

    def __repr__(self):
        return "id: {id} - name: {name}" .format(id=self.id, name=self.username)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'] )
            current_user = UserData.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

            return f(current_user, *args, **kwargs)

    return decorator





if __name__ == '__main__':
    app.run(debug=True)