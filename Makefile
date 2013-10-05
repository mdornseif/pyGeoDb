default: test

test: data
	PYTHONPATH=. python -c 'import doctest; doctest.testfile("README.rst")'

cleanup: # this does NOT convert to python 3.x
	2to3-2.6 -w -f zip -f xreadlines -f xrange -f ws_comma -f throw -f standarderror -f set_literal \
	-f repr -f renames -f reduce -f raise -f paren -f nonzero -f ne -f itertools_imports -f itertools \
	-f isinstance  -f idioms -f has_key -f getcwdu -f filter -f except -f print .

pygeodb/borderdata.py: data/de_landmasse_osm_relation_62781.gpx tools/grenzen2python.py
	PYTHONPATH=. python tools/grenzen2python.py > pygeodb/borderdata.py

pygeodb/plzdata.py: data/DE.tab tools/plz2python2013.py
	PYTHONPATH=. python tools/plz2python2013.py data/DE.tab pygeodb/plzdata.py

data: pygeodb/borderdata.py pygeodb/plzdata.py

maps: data
	#python ./plz_draw --borders maps/deutschland_gebiete.pdf
	python ./plz_draw --borders --width=1440 --height=1920 maps/deutschland_gebiete.png
	#python ./plz_draw --borders maps/deutschland_gebiete.svg
	#python ./plz_draw --borders maps/deutschland_gebiete.eps
	#python ./plz_draw --borders maps/deutschland.ps

	python ./plz_draw --center=250 maps/deutschland.pdf
	python ./plz_draw --center=250 --width=1440 --height=1920 maps/deutschland.png

	python ./plz_draw --borders --acol=42859:#f00 --acol=428:#0f0 --acol=42:#00f maps/42xxx.png
	python ./plz_draw --borders --acol=4:#f00 --acol=3:#0f0 --acol=2:#00f --acol=1:#ff0 --acol=0:#f0f --acol=5:#0ff --acol=6:#07f --acol=7:#f70 --acol=8:#7f7 --acol=9:#70f maps/plzgebiete.png

	python ./plz_draw --borders --cencol=52:#f00 --cencol=50:#00f --cencol=10:#0f0 -c 250 maps/centercolors.png
	python ./plz_draw --borders --acol=40:#ff0 --acol=42:#0ff --acol=45:#0f0 --cencol=52:#f00 --cencol=50:#00f --cencol=10:#0f0 -c 400 -mBielefeld maps/manycolors.png

	python ./plz_draw --center=10 -mBerlin -mHamburg '-mFrankfurt am Main' -mStuttgart -mDortmund -mBremen -mHannover -mLeipzig -mDresden -mBielefeld -mMannheim -mKarlsruhe -mAugsburg -mChemnitz -mKiel '-mHalle' -mMagdeburg '-mFreiburg im Breisgau' -mErfurt -mRostock -mKassel -mPaderborn -mRegensburg -mWolfsburg -mBremerhaven -mIngolstadt -mUlm -mKoblenz -mTrier -mSiegen -mJena -mCottbus -mDüsseldorf -mMünchen -mKöln -mNürnberg -mLübeck -mSaarbrücken -mWürzburg -mGöttingen maps/deutschland_stadte.png

	python ./plz_draw --area --digits=5 --read=data/beispielverteilung.txt maps/beispiel5.png
	python ./plz_draw --area --digits=4 --read=data/beispielverteilung.txt maps/beispiel4.png
	python ./plz_draw --area --digits=3 --read=data/beispielverteilung.txt maps/beispiel3.png
	python ./plz_draw --area --digits=2 --read=data/beispielverteilung.txt maps/beispiel2.png
	python ./plz_draw --area --digits=1 --read=data/beispielverteilung.txt maps/beispiel1.png
	convert maps/beispiel5.png -resize 50% maps/beispiel5_klein.png
	convert maps/beispiel4.png -resize 50% maps/beispiel4_klein.png
	convert maps/beispiel3.png -resize 50% maps/beispiel3_klein.png
	convert maps/beispiel2.png -resize 50% maps/beispiel2_klein.png
	convert maps/beispiel1.png -resize 50% maps/beispiel1_klein.png

clean:
	rm pygeodb/borderdata.py pygeodb/plzdata.py maps/*

upload:
	python setup.py sdist upload

.PHONY: maps data
