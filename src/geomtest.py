'''
This file is a part of BreezyNS - a simple, general-purpose 2D airflow calculator.

Copyright (c) 2013, Brendan Gray

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.



Created on 26 Nov 2013

@author: AlphanumericSheepPig
'''

import pylab
from pycfdmesh.svgloader import beziergonsFromSVG, polygonsFromSVG
from pycfdmesh.geometry import Point, StraightLine



def plotBezierGroup(blist):
    for b in blist:
        points = b.getUniformPointList(20)
        endPoints, controlPoints = b.getDefiningPoints()
        pylab.plot(points.getXs(), points.getYs(),'k-')
        pylab.plot(endPoints.getXs(), endPoints.getYs(),'ko')
        pylab.plot(controlPoints.getXs(), controlPoints.getYs(),'kx')
    pylab.axis('equal')
    

def plotPolygonGroup(polyList, style='k-'):
    for p in polyList:
        points = p.getDefiningPoints()
        pylab.plot(points.getXs(), points.getYs(), style)
        #print(points.length())
    pylab.axis('equal')
        

def testLoadandPlot():
    blist = beziergonsFromSVG('./inputgeometries/arbshape6.svg')
    #pylab.figure('Original Image')
    #plotBezierGroup(blist)
    
    polygonList = []
    for b in blist:
        polygonList.append(b.approximateByPolygon())
                 
    pylab.figure('Polygon Image')
    plotPolygonGroup(polygonList)
    
    pylab.show()
    
    return polygonList[0]
        


def testPolyPointCheck():
    polygons = polygonsFromSVG('./inputgeometries/arbshape7.svg')
    polygon = polygons[0].removeShortLines(0.5).toPolygon()
    print ("Polygon loaded with",len(polygon.lines),"sides.")
    
    
    plist = []
    plist.append(Point(250,210)) # True
    plist.append(Point(140, 150)) # False
    plist.append(Point(280, 320)) # False 
    plist.append(Point(95, 260)) # True
    plist.append(Point(180, 60)) # False

    pylab.figure('Polygon Image')
    plotPolygonGroup([polygon])
    
    for p in plist:   
        print (p, polygon.containsPoint(p))
        pylab.plot(p.x,p.y,'ro')
    
    pylab.show()


def boundingBoxCheck():
    plist = []
    plist.append(Point(250,580))
    plist.append(Point(305, 526))
    plist.append(Point(190, 360))
    plist.append(Point(25, 540))
    plist.append(Point(110, 440))
    
    line1 = StraightLine(plist[0],plist[2])
    line2 = StraightLine(plist[1],plist[4])
    
    print(line1.getBoundingBox() , line2.getBoundingBox())
    print(line1.getBoundingBox() + line2.getBoundingBox())
    print( line1.intersectsWith(line2))
    
    

if __name__ == "__main__":
    #boundingBoxCheck()
    testPolyPointCheck()
    
    
    