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

from __future__ import absolute_import

import math
from pygeodb.plzdata import geodata


class PLZ:
    def __init__(self, plz, land='DE'):
        """The python object for a geolocation"""
        self.plz = plz
        self.land = land
        (self.longitude, self.latitude, self.city) = geodata.get(land.upper(), {}).get(plz, (0, 0, None))
        if not self.city:
            raise ValueError("Unknown PLZ: %s-%s" % (land, plz))

    def __sub__(self, other):
        """Calculates the distance between two geolocations"""
        fLat, fLon = math.radians(self.latitude), math.radians(self.longitude)
        tLat, tLon = math.radians(other.latitude), math.radians(other.longitude)
        distance = math.acos(
            math.sin(tLat) * math.sin(fLat)
            + math.cos(tLat) * math.cos(fLat) * math.cos(tLon - fLon)) * 6380000
        return int(distance)


def _obj2plz(obj):
    if hasattr(obj, 'plz'):
        return PLZ(obj.plz)
    elif hasattr(obj, 'get') and obj.get('plz', None):
        return PLZ(obj['plz'])
    else:
        return PLZ(obj)


def distance(locationa, locationb):
    plza = _obj2plz(locationa)
    plzb = _obj2plz(locationb)
    return plza - plzb


def distances(reference, locations):
    reference = _obj2plz(reference)
    distlist = sorted([(reference - _obj2plz(location), location) for location in locations])
    return distlist


def nearest(reference, locations):
    """Return a sorted list of GeoDBLocation objects. The list is in ascending order
    of the distance relative to the reference location. The reference location must be a
    GeoDBLocation object"""
    return [x[1] for x in distances(reference, locations)]
