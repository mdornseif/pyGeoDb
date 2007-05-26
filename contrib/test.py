#!/opt/local/bin/python2.5

import huGeoDB
from sqlobject import *

if __name__ == "__main__":
    connection_string = 'sqlite:/Users/chris/Programmieren/eclipse/workspace/huGeoDB/src/database2'
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection

    ich = huGeoDB.GeoLocation.select(huGeoDB.GeoLocation.q.Zipcode == huGeoDB.GeoLocation.sqlrepr(50933))
    alex = huGeoDB.GeoLocation.select(huGeoDB.GeoLocation.q.Zipcode == huGeoDB.GeoLocation.sqlrepr(48143))
    md = huGeoDB.GeoLocation.select(huGeoDB.GeoLocation.q.Zipcode == huGeoDB.GeoLocation.sqlrepr(42897))

    # in database stehen zeilenumbrueche hinter den plz...
    # startswith, contains, endswith
    #ich = huGeoDB.GeoLocation.select(huGeoDB.GeoLocation.q.Zipcode.startswith('50933'))
    #alex = huGeoDB.GeoLocation.select(huGeoDB.GeoLocation.q.Zipcode.startswith('48143'))
    #md = huGeoDB.GeoLocation.select(huGeoDB.GeoLocation.q.Zipcode.startswith('42897'))

    print list(ich)
    print list(alex)
    
    ich = ich[0]
    alex = alex[0]
    md = md[0]
    
    print ich - alex
    print alex - ich
    
    print ich - md
    print md - alex
    
    locations = huGeoDB.GeoLocation.select(huGeoDB.GeoLocation.q.Zipcode.startswith('40'))
    
    x = huGeoDB.sort(locations, ich)
    print x
