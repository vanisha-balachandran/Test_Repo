from model import psql_db, City, UserData
from passlib.apps import postgres_context


def insert_data(cities, users):
    # create table
    psql_db.create_tables([City, UserData], safe=True)

    with psql_db.atomic():

        # insert data
        for city in cities:
            track = dict()
            track["name"] = city[1]
            track["countrycode"] = city[2]
            track["district"] = city[3]
            track["population"] = city[4]

            City.create(**track)

    with psql_db.atomic():
        # insert data
        for user in users:
            track = dict()
            track["username"] = user[0]
            track["password_hash"] = postgres_context.encrypt(user[1], user="VANISHA")

            UserData.create(**track)

    print("Done")


if __name__ == '__main__':
    # data
    cities_data = [[1, 'Kabul', 'AFG', 'Kabol', 1780000],
                   [2, 'Qandahar', 'AFG', 'Qandahar', 237500],
                   [3, 'Herat', 'AFG', 'Herat', 186800],
                   [4, 'Mazar-e-Sharif', 'AFG', 'Balkh', 127800],
                   [5, 'Amsterdam', 'NLD', 'Noord-Holland', 731200],
                   [6, 'Rotterdam', 'NLD', 'Zuid-Holland', 593321],
                   [7, 'Haag', 'NLD', 'Zuid-Holland', 440900]]
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