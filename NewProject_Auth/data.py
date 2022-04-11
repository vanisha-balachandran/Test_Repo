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
            track["password_hash"] = postgres_context.encrypt(user[1], user="postgres")

            UserData.create(**track)

    print("Done")


if __name__ == '__main__':
    # data
    cities_data = [[1, 'name1', 'cc1','dis1', 1780000],
                   [2, 'name2', 'cc2', 'dis2', 237500],
                   [3, 'name3', 'cc3', 'dis3', 186800],
                   [4, 'name4', 'cc4', 'dis4', 127800],
                   [5, 'name5', 'cc5', 'dis5', 731200],
                   [6, 'name6', 'cc6', 'dis6', 593321],
                   [7, 'name7', 'cc7', 'dis7', 440900]]
    # sample user data
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