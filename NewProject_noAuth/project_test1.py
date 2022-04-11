from peewee import *

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
        db_table = 'City_table'
        table_alias = 'c'


#setting fields for the class
class City_table(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=35)
    countrycode = CharField(max_length=3)
    district = CharField(max_length=20)
    population = BigIntegerField()


#this function will serialize all the fieldsin the table
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
#connect to the database and create a table
psql_db.connect()
psql_db.create_tables([City_table])

#insert data to the database
def insert_data(cities):
    # create table
    #psql_db.create_tables(City_table, safe=True)

    with psql_db.atomic():
        # insert data
        for city in cities:
            track = dict()
            track["name"] = city[1]
            track["countrycode"] = city[2]
            track["district"] = city[3]
            track["population"] = city[4]

            City_table.create(**track)
    '''
    with psql_db.atomic():
        for data_dict in cities:
            City_table.create(**data_dict)
    print("Done")
'''



if __name__ == '__main__':
    # data
    cities_data = [[1,'name1', 'cc1', 'dis1', 1780000],
                   [2,'name2', 'cc2', 'dis2', 237500],
                   [3,'name3', 'cc3', 'dis3', 186800],
                   [4,'name4', 'cc4', 'dis4', 127800],
                   [5,'name5', 'cc5', 'dis5', 731200],
                   [6,'name6', 'cc6', 'dis6', 593321],
                   [7,'name7', 'cc7', 'dis7', 440900]]

    insert_data(cities_data)