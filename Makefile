default: test

test: data
	PYTHONPATH=. python -c 'import doctest; doctest.testfile("README.rst")'

cleanup: # this does NOT convert to python 3.x
	2to3-2.6 -w -f zip -f xreadlines -f xrange -f ws_comma -f throw -f standarderror -f set_literal \
	-f repr -f renames -f reduce -f raise -f paren -f nonzero -f ne -f itertools_imports -f itertools \
	-f isinstance  -f idioms -f has_key -f getcwdu -f filter -f except -f print .

pygeodb/borderdata.py: data/de_landmasse_osm_relation_62781.gpx tools/grenzen2python.py
	PYTHONPATH=. python tools/grenzen2python.py > pygeodb/borderdata.py

pygeodb/plzdata.py: data/opengeodb_plz.txt tools/plz2python.py
	PYTHONPATH=. python tools/plz2python.py data/opengeodb_plz.txt pygeodb/plzdata.py

data: pygeodb/borderdata.py pygeodb/plzdata.py

maps: data
	python ./plz_draw --borders maps/deutschland_gebiete.pdf
	python ./plz_draw --borders --width=1440 --heigth=1920 maps/deutschland_gebiete.png
	#python ./plz_draw --borders maps/deutschland_gebiete.svg
	#python ./plz_draw --borders maps/deutschland_gebiete.eps
	#python ./plz_draw --borders maps/deutschland.ps

	python ./plz_draw --center=250 maps/deutschland.pdf
	python ./plz_draw --center=250 --width=1440 --heigth=1920 maps/deutschland.png

	python ./plz_draw --center=10 -mBerlin -mHamburg '-mFrankfurt am Main' -mStuttgart -mDortmund -mBremen -mHannover -mLeipzig -mDresden -mBielefeld -mMannheim -mKarlsruhe -mAugsburg -mChemnitz -mKiel '-mHalle' -mMagdeburg '-mFreiburg im Breisgau' -mErfurt -mRostock -mKassel -mPaderborn -mRegensburg -mWolfsburg -mBremerhaven -mIngolstadt -mUlm -mKoblenz -mTrier -mSiegen -mJena -mCottbus -mDüsseldorf -mMünchen -mKöln -mNürnberg -mLübeck -mSaarbrücken -mWürzburg -mGöttingen maps/deutschland_stadte.pdf
	python ./plz_draw --area --digits=5 --read=data/beispielverteilung.txt maps/beispiel5.pdf
	python ./plz_draw --area --digits=4 --read=data/beispielverteilung.txt maps/beispiel4.pdf
	python ./plz_draw --area --digits=3 --read=data/beispielverteilung.txt maps/beispiel3.pdf
	python ./plz_draw --area --digits=2 --read=data/beispielverteilung.txt maps/beispiel2.pdf
	python ./plz_draw --area --digits=1 --read=data/beispielverteilung.txt maps/beispiel1.pdf

clean:
	rm pygeodb/borderdata.py pygeodb/plzdata.py maps/*

.PHONY: maps data
