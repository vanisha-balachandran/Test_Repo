from peewee import *
from passlib.apps import postgres_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from app import *

#create a PostgreSQL database
psql_db = PostgresqlDatabase(
    'NewProject_DB',
    user='postgres',
    password='srisai@2005',
    host='localhost',
)

#create a table class to the database
class BaseModel(Model):

    class Meta:
        database = psql_db
        db_table = 'Auth_table'
        table_alias = 'c'


#setting fields for the class
class Auth_table(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=35)
    countrycode = CharField(max_length=3)
    district = CharField(max_length=20)
    population = BigIntegerField()


#this function will serialize all the fields in the table as per the schema
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


#setting class for User & password table
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

    def hash_password(self):
        self.password_hash = postgres_context.encrypt(self.password_hash, user="postgres")

    def verify_password(self, password):
        return postgres_context.verify(password, self.password_hash, user="postgres")

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = UserData.get(UserData.id == data['id'])
        return user

    class Meta:
        database = psql_db

#connect to the database and create a table
psql_db.connect()
psql_db.create_tables([Auth_table, UserData], safe=True)

#insert data to the database
def insert_data(cities, users):
    # create table
    #psql_db.create_tables(Auth_table, safe=True)

    with psql_db.atomic():
        # insert data
        for city in cities:
            track = dict()
            track["name"] = city[1]
            track["countrycode"] = city[2]
            track["district"] = city[3]
            track["population"] = city[4]

            Auth_table.create(**track)


    with psql_db.atomic():
        # insert data
        for user in users:
            track = dict()
            track["username"] = user[0]
            track["password_hash"] = postgres_context.encrypt(user[1], user="postgres")

            UserData.create(**track)

    print("Done")



if __name__ == '__main__':
    # data
    cities_data = [[1,'name1', 'cc1', 'dis1', 1780000],
                   [2,'name2', 'cc2', 'dis2', 237500],
                   [3,'name3', 'cc3', 'dis3', 186800],
                   [4,'name4', 'cc4', 'dis4', 127800],
                   [5,'name5', 'cc5', 'dis5', 731200],
                   [6,'name6', 'cc6', 'dis6', 593321],
                   [7,'name7', 'cc7', 'dis7', 440900]]

    users = [
        ["USER1", "xxx"],
        ["USER2", "yyy"],
        ["USER3", "aaa"],
        ["USER4", "bbb"],
        ["USER5", "ccc"],
        ["USER6", "mmm"],
        ["USER7", "nnn"],
        ["VANISHA", "mypass"],
    ]

    insert_data(cities_data, users)