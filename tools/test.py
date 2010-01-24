#!/opt/local/bin/python2.5

import pygeodb
from sqlobject import *

if __name__ == "__main__":
    connection_string = 'sqlite:///Users/md/code2/git/pyGeoDb/database.db'
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection

    ich = pygeodb.GeoLocation.select(pygeodb.GeoLocation.q.Zipcode == pygeodb.GeoLocation.sqlrepr(50933))
    alex = pygeodb.GeoLocation.select(pygeodb.GeoLocation.q.Zipcode == pygeodb.GeoLocation.sqlrepr(48143))
    md = pygeodb.GeoLocation.select(pygeodb.GeoLocation.q.Zipcode == pygeodb.GeoLocation.sqlrepr(42897))

    # in database stehen zeilenumbrueche hinter den plz...
    # startswith, contains, endswith
    #ich = pygeodb.GeoLocation.select(pygeodb.GeoLocation.q.Zipcode.startswith('50933'))
    #alex = pygeodb.GeoLocation.select(pygeodb.GeoLocation.q.Zipcode.startswith('48143'))
    #md = pygeodb.GeoLocation.select(pygeodb.GeoLocation.q.Zipcode.startswith('42897'))

    print(list(ich))
    print(list(alex))

    ich = ich[0]
    alex = alex[0]
    md = md[0]

    print(ich - alex)
    print(alex - ich)

    print(ich - md)
    print(md - alex)

    locations = pygeodb.GeoLocation.select(pygeodb.GeoLocation.q.Zipcode.startswith('40'))

    x = pygeodb.sort(locations, ich)
    print(x)
