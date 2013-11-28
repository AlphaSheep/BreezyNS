'''
Created on 26 Nov 2013

@author: AlphanumericSheepPig
'''

import pylab
from pycfdmesh.svgloader import beziergonsFromSVG



def plotBezierGroup(blist):
    for b in blist:
        points = b.getUniformPointList(20)
        endPoints, controlPoints = b.getDefiningPoints()
        pylab.plot(points.getXs(), points.getYs(),'k-')
        pylab.plot(endPoints.getXs(), endPoints.getYs(),'ko')
        pylab.plot(controlPoints.getXs(), controlPoints.getYs(),'kx')
    pylab.axis('equal')
    

def plotPolygonGroup(polyList):
    for p in polyList:
        points = p.getDefiningPoints()
        pylab.plot(points.getXs(), points.getYs(),'ko-')
        print(points.length())
    pylab.axis('equal')
        

def test2():
    blist = beziergonsFromSVG('./inputgeometries/arbshape6.svg')
    #pylab.figure('Original Image')
    #plotBezierGroup(blist)
    
    polygonList = []
    for b in blist:
        polygonList.append(b.approximateByPolygon())
                 
    pylab.figure('Polygon Image')
    plotPolygonGroup(polygonList)
    
    pylab.show()
        



test2()