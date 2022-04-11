from peewee import *

psql_db = PostgresqlDatabase(
    'NewProject_DB',
    user='postgres',
    password='srisai@2005',
    host='localhost',
)


class BaseModel(Model):

    class Meta:
        database = psql_db
        db_table = 'City_table'
        table_alias = 'c'


class City_table(BaseModel):
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