PyGeoDb - an Interface to OpenGeoDb
===================================

PyGeoDb is an Python interface to OpenGeoDb_. It is all about Austrian, German
and Swiss postcodes (ZIPs) and city locations. It requires Python 2.6.
The rest of this documentation is in German language. Probably you can extend
the system to US data by integrating US data as used in Ben Fry's zipdecode_.

You can download the latest release at http://pypi.python.org/pypi/pyGeoDb/#, development releases are available at http://github.com/mdornseif/pyGeoDb#.

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
.. _zipdecode: http://benfry.com/zipdecode/
.. _Umkreissuche: http://de.wikipedia.org/wiki/Umkreissuche
.. _GeoClassPHP: http://sourceforge.net/projects/geoclassphp/


Entfernungen
------------


Entfernungsberechnung
~~~~~~~~~~~~~~~~~~~~~

PyGeoDb kann die Entfernung in Metern zwischen zwei Postleitzahlenbereichen
berechnen. Dazu kann direkt eine Postleitzahl als String, ein dict, oder ein
Objekt, dass dem AddressProtocol_ entspricht, uebergeben werden::

    >>> import pygeodb
    >>> pygeodb.distance("42897", "50933") # strings
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
------------------

.. _hyperlink-name: karten

pyGeoDb kann Postleitzhalenkarten generieren. Dazu kommt die Graphikbibliothek
Pycairo_ zum Einsatz, die natuerlich vorher installiert sein muss. Karten
koennen im PDF_, PNG_, EPS und SVG Format erstellt werden.

.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/deutschland.png
.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/deutschland_gebiete.png
.. image:: http://static.23.nu/md/Pictures/plz_einfaerben.png
.. image:: http://static.23.nu/md/Pictures/plz_flaechen.png
.. image:: http://static.23.nu/md/Pictures/plz_deutschland_gebiete.png
.. image:: http://static.23.nu/md/Pictures/ZZ625F1174.png

Es gibt keine freie Datenquelle zu Groesse und Form der einzelnen
Postleitzahlenbereiche. Jedoch kann man sich der Form der
Postleitzahlenbereiche annaehern, indem man ein `Voronoi-Diagramm`_ erzeugt.
Dies weicht im Detail zwar deutlich von den realen Postleitzahlenbereichen ab,
reicht aber fuer Visualisierungsaufgaben aus. Zur Erzeugung des Graphen, der
die Postleitzahlenbereiche unterteilt, wird der "Fortune Algorithmus"
werwendet.

Rufen Sie ``./plz_draw --help`` auf, um die Aufrufparameter angezeigt zu
bekommen. Beispieldateien kann man durch das Kommando `make maps` erstellen -
die entsprechenden Kommandos finden sich in der Datei Makefile, unten.

.. _Pycairo: http://cairographics.org/pycairo/
.. _PDF: https://github.com/mdornseif/pyGeoDb/raw/master/maps/deutschland_gebiete.pdf
.. _PNG: https://github.com/mdornseif/pyGeoDb/raw/master/maps/deutschland_gebiete.png
.. _`Voronoi-Diagramm`: http://de.wikipedia.org/wiki/Voronoi-Diagramm
.. _voronoiexample1: http://www.raymondhill.net/voronoi/voronoi.php
.. _voronoiexample2: http://www.diku.dk/hjemmesider/studerende/duff/Fortune/

Eine deutsche Postleitzahlenkarte erstellt man beispielsweise mit folgenden
Kommandos::

    # Deutschlandkarte mit Postleitzahlenbereichen
    $ python ./plz_draw --borders --acol=4:#f00 --acol=3:#0f0 --acol=2:#00f \
    --acol=1:#ff0 --acol=0:#f0f --acol=5:#0ff --acol=6:#07f --acol=7:#f70 \
    --acol=8:#7f7 --acol=9:#70f test.pdf

.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/plzgebiete.png.png

    # 42859 und darueberliegende Bereiche markieren
    $ python ./plz_draw --borders --acol=42859:#f00 --acol=428:#0f0 \
    --acol=42:#00f test.pdf

.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/42xxx.png

Man kann stattdessen auch die Mittelpunkte der Postleitzahlengebiete markieren.
Dabei gibt man mit `-c 250` die grösse der Punkte an.

    python ./plz_draw --borders --cencol=52:#f00 --cencol=50:#00f --cencol=10:#0f0 -c 250 maps/centercolors.png

.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/centercolors.png

Natürlich kann man das auch alles mischen.

    python ./plz_draw --borders --acol=40:#ff0 --acol=42:#0ff --acol=45:#0f0 --cencol=52:#f00 --cencol=50:#00f --cencol=10:#0f0 -c 400 -mBielefeld maps/manycolors.png

.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/manycolors.png


Man kann auf der Karte Ortsnamen anzeigen lassen. Wenn ein Ort mehrere
Postleitzahlen hat, wird der Ortsname am gemittelten Zentrum der verschiedenen
Postleitzahlenbereiche gezeichnet. Eine Karte mit dem meissten deutschen
Grossstaedten erhaelt man mit folgendem Kommando::

    python ./plz_draw -mBerlin -mHamburg -mStuttgart -mDortmund -mBremen
    -mHannover -mLeipzig -mDresden -mBielefeld -mMannheim -mKarlsruhe
    -mAugsburg -mChemnitz -mKiel -mHalle -mMagdeburg -mErfurt -mRostock
    -mKassel -mPaderborn -mRegensburg -mWolfsburg -mBremerhaven -mIngolstadt
    -mUlm -mKoblenz -mTrier -mSiegen -mJena -mCottbus '-mFreiburg im Breisgau'
    '-mFrankfurt am Main' test.pdf

Die Eigabe der Staedtenamen mit Umlauten ist je nach Konfiguration des
Betriebssystems problematisch. Auch lassen sich diese in dieser Hilfedatei
nicht problemlos darstellen. Sie koennen die Parameter ``-mDuesseldorf
-mMuenchen -mKoeln -mNuernberg -mLuebeck -mSaarbruecken -mWuerzburg
-mGoettingen`` wenn Sie jeweils die korrekten Umlaute einsetzen.

.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/deutschland_stadte.png

Paramerisierte Kartenfaerbung
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Das Programm kann auch Postleitzahlenbereiche je nach Haeufigkeit des
Aufkommens von Postleitzahlen in einer Datei einfaerben. Das ist z.B. Karten,
die die Kundenverteilung ider dergleichen visualisieren, geeignet.

Erzeugen Sie datzu eineTatei mit Test-Postleitzahlen. Schreiben Sie z.B
folgendes in eine Datei test.txt::

    42477
    42477
    42477
    42477
    42897
    42897
    42897
    42499
    42859
    42899
    42929

Nun kann man diese Daten nutzen, um eine Entsprechend eingefaerbte Karte zu
erstellen::

    # eingefaerbte Gebiete
    python ./plz_draw --read=test.txt --areas test.pdf

42477 wird am dunkelsten eingefaerbt (kommt 4 x vor), 42897 dunkel (kommt 3 x
vor) die restlichen Felder werden nur leicht eingefaerbt. Fuer Tests sind
Beispieldaten in data/beispielverteilung.txt beigelegt.

Solange Sie nicht sehr grosse Datenbestaende, von mehr als einer halben
Million Datensaetze haben, werden die Eingefaerbten Karten recht
unregelmaessig aussehen. Dem kann man entgegenwirken, indem man die Daten von
Postleitzahlenbereichen mit gleichem Prefix zusammenfasst, um ein
gleichmaessigeres Ergebnis zu erzielen. Dies geht mit dem Parameter
``--digits``. Wenn Sie ``--digits=3`` uebergeben, werden nur die ersten drei
Ziffern der Postleitzahl zur Zusammenfassung verwendet. Geben sie ``make
maps`` ein, und schauen Sie die fuenf Dateien ``maps/beispiel?.pdf`` an, um
die Auswirkung des ``--digits``-Parameters zu sehen.

.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/beispiel5_klein.png
.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/beispiel4_klein.png
.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/beispiel3_klein.png
.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/beispiel2_klein.png
.. image:: https://raw.github.com/mdornseif/pyGeoDb/master/maps/beispiel1_klein.png


Autoren
-------

Der urspruengliche Entfernungsberechnungscode wurde in 2007 von Christian N
Klein entwickelt. Die Voronoi Berechnung basiert auf Code von Steve Fortune,
der von Shane O'Sullivan in C++ und dann von Bill Simons in Python konvertiert
wurde.

Die Datengrundlage fuer die Polstleitzahlenbereiche stammt vom `OpenGeoDb
Projekt`_. Die deutschen Grenzen stammen aus `Openstreetmap Project Germany`_.

Die Kartengenerierung stammt von Maximillian Dornseif und basiert auf seinem
Projekt `zipdecodede`, dass auf Code aus Ben Frys Buch `Visualizing Data`_
beruht.

.. _`OpenGeoDb Projekt`: http://www.opengeodb.de
.. _`Openstreetmap Project Germany`: http://wiki.openstreetmap.org/wiki/WikiProject_Germany/Grenzen#Deutschland
.. _`zipdecodede`: http://md.hudora.de/c0de/zipdecodeDE/
.. _`Visualizing Data`: http://www.librarything.com/work/4108432/book/37543244


Alternativen, Quellen & Vermischtes
-----------------------------------

`d9t.gis`_ ist ein sehr Zope-Lastiges Python Projekt zur Entfernugnsberechnung
mit OpenGeoDb Daten. `ruby-opengeodb`_ erlaubt Zugriff auf die OpenGeoDB Daten
aus Ruby heraus.

Es gibt jede Menge Online-Distanzberechnungsdienste, z.B:

 * http://www.edith-distance.de/pdf/doku.pdf
 * http://www.ebaas.de/ebaas-distance-faq/
 * http://www.internet-marketing-service.eu/?id=20
 * http://www.mprobst.de/OpenGeoNearestNeighbours/website/index.html

Umfangreiche Informationen zum deutschen Postleitzahlensystem inklusive freier
Rasterkarten gibt es bei Wikipedia_.

.. _`d9t.gis`: http://pypi.python.org/pypi/d9t.gis
.. _`ruby-opengeodb`: http://ruby-opengeodb.rubyforge.org/
.. _Wikipedia: http://de.wikipedia.org/wiki/Postleitzahl_(Deutschland)

Als Alternative Quelle fuer die Deutschen Grenzen kaeme anstatt von
OpenStreetmap auch NaturalEarth_ in Frage. Geonames_ koennte als Alternative
Quelle fuer Postleitzahlen dienen.

.. _NaturalEarth: http://www.naturalearthdata.com/
.. _Geonames: http://www.geonames.org/postal-codes/

Wenn Sie einen Fehler bemerken, melden Sie Ihn bitte unter http://github.com/mdornseif/pyGeoDb/issues


.. image:: https://d2weczhvl823v0.cloudfront.net/mdornseif/pygeodb/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

