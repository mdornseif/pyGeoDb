#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by Christioan Klein in 2007
# BSD licensed

"""
1) alle GeoLocations in einem PLZ-Gebiet:

GeoLocation.select(GeoLocation.q.Zipcode == zipcode)
oder
GeoLocation.select(GeoLocation.q.Zipcode.startswith(zipcode))

2) Distanz zwischen zwei GeoLocations

geoloc_1 = GeoLocation.select()[0]
geoloc_2 = GeoLocation.select()[0]

distance = geoloc_1 - geoloc_2
(Reihenfolge spielt keine Rolle)

3) GeoLocations sortiert nach Distanz zu einem Referenzpunkt:

referenz = GeoLocation.select()[0]
locations = GeoLocation.select()

distanz_liste = sort(locations, referenz)
"""

import math
import operator
from pygeodb.plzdata import geodata

class PLZ:
    def __init__(self, plz, land='de'):
        """The python object for a geolocation"""
        self.zipcode = plz
        self.country = land
        (self.longitude, self.latitude, self.city) = geodata.get(land.lower(), {}).get(plz, (0, 0, None))
        if not self.city:
            raise ValueError("Unknown PLZ: %s-%s" % (land, plz))

    def __sub__(self, other):
        """Calculates the distance between two geolocations"""
        fLat, fLon = math.radians(self.latitude), math.radians(self.longitude)
        tLat, tLon = math.radians(other.latitude), math.radians(other.longitude)
        distance = math.acos(math.sin(tLat) * math.sin(fLat) 
                             + math.cos(tLat) * math.cos(fLat) * math.cos(tLon
                             - fLon)) * 6380
        return distance


def sort(locations, reference):
    """Return a sorted list of GeoDBLocation objects. The list is in ascending order
    of the distance relative to the reference location. The reference location must be a
    GeoDBLocation object"""

    distances = {}
    for location in locations:
        #distances[location.id] = reference - location
        distances[location.zipcode] = reference - location

    items = distances.items()
    items.sort(key = operator.itemgetter(1))
    return items


#print PLZ('42477') - PLZ('50126'), "km"
#print vars(PLZ('50126'))