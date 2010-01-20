PyGeoDb - an Interfact op OpenGeoDb
===================================

PyGeoDb is an Python Interface to OpenGeoDb_. It is all about Austrian, German
and Swiss Postcodes and City location. It requires Python 2.6.
The rest of this documentation is in german Language.

Die ist ein Python Interface zu OpenGeoDb. "Im Mittelpunkt des Projektes
OpenGeoDB steht der Aufbau einer moeglichst vollstaendigen Datenbank mit
Geokoordinaten zu allen Orten und Postleitzahlen (bisher: A,B,CH,D und FL)."
(OpenGeoDB Wiki) Die Datenbank wird ueberwiegend zur Umkreissuche_ oder zur
(groben) Geocodierung verwendet. In der PHP-Welt wird es fast ausschliesslich
mit GeoClassPHP_ verwendet. Fuer Python gibt es bisher keine weit verbreitete
Loesung.

Zusaetzlich hilft PyGeoDb bei der Erstellung zon Postleitzahlen Karten. Dazu
werden neben den OpenGeoDb Daten auch Informationen aus Openstreetmap
herangezogen.

.. _OpenGeoDb: http://opengeodb.giswiki.org/
.. _Umkreissuche: http://de.wikipedia.org/wiki/Umkreissuche
.. _GeoClassPHP: http://sourceforge.net/projects/geoclassphp/


Nutzung
-------


Entfernungsberechnung
~~~~~~~~~~~~~~~~~~~~~

PyGeoDb kann die Entfernung in Metern zwischen zwei Postleitzahlenbereichen
berechnen. Dazu kann direkt eine Postleitzahl als String, ein dict, oder ein
Objekt, dass dem AddressProtocol_ entspricht, uebergeben werden::

    >>> import pygeodb
    >>> pygeodb.distance("42897", "50933") # Strings
    38131

    >>> pygeodb.distance({'plz': "42897"}, {'plz': "48143"}) # dicts
    90478

    >>> class LocationObject(object): pass
    >>> loc = LocationObject()
    >>> loc.plz = "50933"
    >>> pygeodb.distance(loc, "48143") # Objekte
    124737


Sortieren nach Entfernung
~~~~~~~~~~~~~~~~~~~~~~~~~

pyGeoDb kann eine Liste von Postleitzahlen nach der Entfernung zu einer
bestimmten Postleitzahl sortieren. Dabei koennen, Strings sowie Dicts und
Objekte nach dem AddressProtocol gemischt werden::

    >>> pygeodb.nearest("42897", ["42477", "48143", {'plz': "45149"}, loc]) #doctest: +ELLIPSIS
    ['42477', {'plz': '45149'}, <__main__.LocationObject object ...>, '48143']

Wenn es relevant ist, wie weit die verschiedenen Postleitzahlen entfernt sind,
kann auch dies mit zurueck gegeben werden::

    >>> pygeodb.distances("42897", ["50933", "42477", "48143", "45149", "42897"])
    [(0, '42897'), (7200, '42477'), (34466, '45149'), (38131, '50933'), (90478, '48143')]

.. _AddressProtocol: http://github.com/hudora/huTools/blob/master/doc/standards/address_protocol.markdown


Fehlerbehandlung
~~~~~~~~~~~~~~~~

Wenn eine Postleitzahl unbekannt ist, wird eine ValueError() Exception
ausgeloesst::

    >>> pygeodb.distance("42897", "99999") # Strings
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    ValueError: Unknown PLZ: DE-99999


Kartengeneriertung
~~~~~~~~~~~~~~~~~~

pyGeoDb kann Postleitzhalenkarten generieren. Dazu kommt die Graphikbibliothek
Pycairo_ zum Einsatz, die natuerlich vorher installiert sein muss. Karten
koennen im PDF_, PNG_, EPS_ und SVG_ Format erstellt werden.

Es gibt keine freie Datenquelle zu Groesse und Form der einzelnen
Postleitzahlenbereiche. Jedoch kann man sich der Form der
Postleitzahlenbereiche annaehern, indem man ein `Voronoi-Diagramm`_ erzeugt.
Dies weicht im Detail zwar deutlich von den realen Postleitzahlenbereichen ab,
reicht aber fuer Visualisierungsaufgaben aus. Zur Erzeugung des Graphen, der
die Postleitzahlenbereiche unterteilt, wird der "Fortune Algorithmus"
werwendet.

Rufen Sie `./plz_draw --help` auf, um die Aufrufparameter angezeigt zu
bekommen. Beispieldateien kann man durch das Kommando `make maps` erstellen -
die entsprechenden kommandos finden sich in der Datei Makefile unten.

.. _Pycairo: http://cairographics.org/pycairo/ 
.. _PDF: https://github.com/mdornseif/pyGeoDb/raw/master/maps/deutschland_gebiete.pdf
.. _PNG: https://github.com/mdornseif/pyGeoDb/raw/master/maps/deutschland_gebiete.png
.. _EPS: https://github.com/mdornseif/pyGeoDb/raw/master/maps/deutschland_gebiete.svgz
.. _SVG: https://github.com/mdornseif/pyGeoDb/raw/master/maps/deutschland_gebiete.eps.gz
.. _`Voronoi-Diagramm`: http://de.wikipedia.org/wiki/Voronoi-Diagramm
.. _voronoiexample1: http://www.raymondhill.net/voronoi/voronoi.php
.. _voronoiexample2: http://www.diku.dk/hjemmesider/studerende/duff/Fortune/

.. image:: https://github.com/mdornseif/pyGeoDb/raw/master/maps/deutschland_small.png

Autoren
-------

Der urspruengliche Entfernungsberechnungscode wurde in 2007 von Christian N
Klein entwickelt. Die Voronoi Berechnung basiert auf Code von Steve Fortune,
der von Shane O'Sullivan in C++ und dann von Bill Simons in Python konvertiert
wurde.

Die Datengrundlage fuer die Polstleitzahlenbereiche stammt vom `OpenGeoDb
Projekt`_. Die Deutschen grenzen stammen aus `Openstreetmap Project Germany`_.

Die Kartengenerierung stammt von Maximillian Dornseif und basiert auf seinem
Projekt `zipdecode.de`, dass auf Code aus Ben Frys Buch `Visualizing Data`_
beruht.

.. _`OpenGeoDb Projekt`: http://www.opengeodb.de
.. _`Openstreetmap Project Germany`: http://wiki.openstreetmap.org/wiki/WikiProject_Germany/Grenzen#Deutschland
.. _`zipdecode.de`: http://md.hudora.de/c0de/zipdecodeDE/
.. _`Visualizing Data`: http://www.librarything.com/work/4108432/book/37543244


Alternativen, Quellen & Vermischtes
-----------------------------------

`d9t.gis`_ ist ein sehr Zope-Lastiges Python Projekt zur Entfernugnsberechnung
mit OpenGeoDb Daten.

Es gibt jede Menge Online-Distanzberechnungsdienste, z.B:

 * http://www.edith-distance.de/pdf/doku.pdf
 * http://www.ebaas.de/ebaas-distance-faq/
 * http://www.internet-marketing-service.eu/?id=20
 * http://www.mprobst.de/OpenGeoNearestNeighbours/website/index.html

Umfangreiche Informationen zum deutschen Postleitzahlensystem inklusive freier
Rasterkarten gibt es bei Wikipedia_.

.. _`d9t.gis`: http://pypi.python.org/pypi/d9t.gis
.. _Wikipedia: http://de.wikipedia.org/wiki/Postleitzahl_(Deutschland)

Wenn Sie einen Fehler bemerken, melden Sie Ihn bitte unter http://github.com/mdornseif/pyGeoDb/issues
