from model import psql_db, City_table


def insert_data(cities):
    # create table
    psql_db.create_tables(City_table, safe=True)

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