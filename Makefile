default: pygeodb/borderdata.py pygeodb/plzdata.py

cleanup:
	2to3-2.6 -w -f zip -f xreadlines -f xrange -f ws_comma -f throw -f standarderror -f set_literal \
	-f repr -f renames -f reduce -f raise -f paren -f nonzero -f ne -f itertools_imports -f itertools \
	-f isinstance  -f idioms -f has_key -f getcwdu -f filter -f except .

pygeodb/borderdata.py: data/de_landmasse_osm_relation_62781.gpx tools/grenzen2python.py
	PYTHONPATH=. python tools/grenzen2python.py > pygeodb/borderdata.py

pygeodb/plzdata.py: data/opengeodb_plz.txt tools/plz2python.py
	PYTHONPATH=. python tools/plz2python.py < data/opengeodb_plz.txt > pygeodb/plzdata.py

maps:
	PYTHONPATH=. python tools/plz_draw --frontier --voronoi maps/deutschland_gebiete.pdf
	PYTHONPATH=. python tools/plz_draw --frontier --voronoi --width=1440 --heigth=1920 maps/tmp.png
	pngcrush maps/tmp.png maps/deutschland_gebiete.png
	PYTHONPATH=. python tools/plz_draw --frontier --voronoi maps/deutschland_gebiete.svg
	gzip -c < maps/deutschland_gebiete.svg >  maps/deutschland_gebiete.svgz
	PYTHONPATH=. python tools/plz_draw --frontier --voronoi maps/deutschland_gebiete.eps
	gzip -c < maps/deutschland_gebiete.eps > maps/deutschland_gebiete.eps.gz
	#PYTHONPATH=. python tools/plz_draw --frontier --voronoi maps/deutschland.ps

	PYTHONPATH=. python tools/plz_draw --frontier --center=250 maps/deutschland.pdf
	PYTHONPATH=. python tools/plz_draw --frontier --center=250 --width=1440 --heigth=1920 maps/tmp.png
	pngcrush maps/tmp.png maps/deutschland.png
	PYTHONPATH=. python tools/plz_draw --frontier --center=250 maps/deutschland.svg
	gzip -c < maps/deutschland.svg >  maps/deutschland.svgz
	PYTHONPATH=. python tools/plz_draw --frontier --center=250 maps/deutschland.eps
	gzip -c < maps/deutschland.eps > maps/deutschland.eps.gz
	#PYTHONPATH=. python tools/plz_draw --frontier --voronoi maps/deutschland.ps
	rm maps/tmp.png  maps/*.svg maps/*.eps

.PHONY: maps
