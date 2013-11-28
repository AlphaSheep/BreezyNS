'''
Created on 27 Nov 2013

@author: AlphanumericSheepPig
'''

import pylab
from pycfdmesh.mesh import Mesh
from pycfdmesh.geometry import Point
# from pycfdmesh.svgloader import polygonsFromSVG


def plotMesh(mesh):
    pylab.figure()
    for element in mesh.elements:
        points = element.getPointList()
        pylab.plot(points.getXs(), points.getYs(),'k-')
    pylab.axis('equal')
    pylab.show()
    
    
    
def test():
    bottomLeft = Point(0,0)
    mesh = Mesh(bottomLeft, 10, 10, 100, 1)
    print("Mesh generated\n")
    mesh.getElementAtPoint(Point(320,220)).split()
    mesh.getElementAtPoint(Point(320,220)).split()
    mesh.getElementAtPoint(Point(320,220)).split()
    mesh.getElementAtPoint(Point(320,220)).split()
    mesh.getElementAtPoint(Point(320,220)).split()
    mesh.getElementAtPoint(Point(320,220)).split()
    plotMesh(mesh)
    
    
from pycfdmesh.svgloader import beziergonsFromSVG



test()