#!/usr/bin/env python
import random, math, sys
from optparse import OptionParser
import cairo
import pygeodb

def intRGB(r, g, b):
        return (r/255.0, g/255.0, b/255.0)

HIGHLIGHT=intRGB(0xff, 0x72, 0x72)

class NiceCtx(cairo.Context):
    defaultBorderColour = intRGB(0x7d, 0x7d, 0x7d)
    def stroke_border(self, border):
        src = self.get_source()
        width = self.get_line_width()
        self.set_source_rgba(*self.defaultBorderColour)
        self.stroke_preserve()
        self.set_source(src)
        self.set_line_width(width - (border * 2))
        self.stroke()
        
    def init_geoscale(self, minx, xwidth, miny, yheigth):
        self.minx = minx
        self.miny = miny
        self.xwidth = xwidth
        self.yheigth = yheigth
        self.geoscalefactor = 1 / max([xwidth, yheigth])
        self.geoscalefactor = self.geoscalefactor
        
    def geoscale(self, x, y):
        # we use 1.35 for a very simple "projection"
        return (x-self.minx)*self.geoscalefactor, ((y-self.miny)*self.geoscalefactor*-1.35) + 1.35


class Canvas:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.surface = cairo.PDFSurface('test.pdf', width, height)
        self.background(1, 1, 1)

    def ctx(self):
        context = NiceCtx(self.surface)
        self.ctxscale = min([self.width, self.height])
        context.scale(self.ctxscale, self.ctxscale)
        self.ctxscale = 1/float(self.ctxscale)
        return context

    def background(self, r, g, b):
        c = self.ctx()
        c.set_source_rgb(r, g, b)
        c.rectangle(0, 0, self.width, self.height)
        c.fill()
        c.stroke()

    def save(self, fname, vertical):
        surf = self.surface
        #surf.write_to_png(fname)

c = Canvas(480, 640)
ctx = c.ctx()
ctx.set_line_cap(cairo.LINE_CAP_ROUND)
ctx.set_line_join(cairo.LINE_JOIN_ROUND)
# ctx.set_source_rgb(*HIGHLIGHT)

geoitems = pygeodb.geodata['de'].items()

# find desired image size
x = []
y = []
for plz, (long, lat, name) in geoitems:
    x.append(long)
    y.append(lat)
ctx.init_geoscale(min(x), max(x)-min(x), min(y), max(y)-min(y))
ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
ctx.set_line_width(1*c.ctxscale)
# ctx.stroke_border(self.border)


# see http://lists.cairographics.org/archives/cairo/2009-June/017459.html for drawing points
for plz, (long, lat, name) in geoitems:
    print ctx.geoscale(long, lat)
    ctx.move_to(*ctx.geoscale(long, lat))
    ctx.close_path()

ctx.stroke()
ctx.fill()

