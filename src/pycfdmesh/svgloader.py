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



Created on 27 Nov 2013

@author: AlphanumericSheepPig

This module provides some functions for loading paths in svg files into the Beziergon objects provided by the
pycfdmesh.geometry module.

The svg files may be created in any compatible program (e.g. Inkscape).
This module is very limited - it ignores anything in the file that is not a path, and looks only at the path 
definition, ignoring any style that is specified.

Only a limited subset of path commands available in the svg pecification have been implemented. The
relative and absolute forms of the following commands are supported:
    - moveto
    - closepath
    - lineto
    - curveto
'''


from xml.dom import minidom
from pycfdmesh.geometry import Point, CubicBezier, Beziergon



def beziergonsFromSVG(filename):
    '''
    Takes the name of an svg file, and returns a list of Beziergon objects generated from paths defined in the file.
    '''
    svgfile = minidom.parse(filename)
    height = float(svgfile.getElementsByTagName('svg')[0].attributes['height'].value.strip())
    pathObjList = svgfile.getElementsByTagName('path')
    
    beziergonList = []
    
    for p in pathObjList:
        pathStr = p.attributes['d'].value
        curveStrList = pathStr.split(' ')
        currentPoint = Point (0,0)
        nextPoint = Point (0,0)
        relative = False
        curveType = 'start'
        pointType = 'end'
        curveBezierList = []
        for c in curveStrList:
            if not c.upper() in ['M','C','Z','L']:
                p = c.split(',')
                nextPoint = Point(float(p[0].strip()), float(p[1].strip()))
                if relative:
                    nextPoint = currentPoint + nextPoint
                
                if curveType == 'start':
                    currentPoint = nextPoint
                    curveType = 'line'
#                    print('Jumping to', currentPoint.switchReference(height))
                    
                
                elif curveType == 'cubic':
                    if pointType == 'end':
                        pointType = 'control1'
                        startPoint = currentPoint.switchReference(height)
                        firstControl = (nextPoint).switchReference(height)
                        
#                        print('Starting curve from', startPoint, 'with first control', firstControl)
                    elif pointType == 'control1':
                        pointType = 'control2'
                        secondControl = (nextPoint).switchReference(height)
#                        print('    Next control', secondControl)
                    elif pointType == 'control2':
                        pointType = 'end'
                        currentPoint = nextPoint
                        endPoint = currentPoint.switchReference(height)
#                        print('    Ending curve at', endPoint)
                        curveBezierList.append(CubicBezier(startPoint, firstControl, secondControl, endPoint))
                        
                elif curveType == 'line':
                    startPoint = currentPoint.switchReference(height)
                    currentPoint = nextPoint
                    endPoint = currentPoint.switchReference(height)
#                    print('Inserting line from', startPoint, 'to', endPoint)
                    curveBezierList.append(CubicBezier(startPoint, startPoint, endPoint, endPoint))
                    
            else:
                if c==c.lower():
                    relative = True
                else:
                    relative = False
                if c.upper() == 'M':
                    curveType = 'start'
                elif c.upper() == 'L':
                    curveType = 'line'
                elif c.upper() == 'C':
                    curveType = 'cubic'
                elif c.upper() == 'Z':
                    startPoint = curveBezierList[-1].p3
                    endPoint = curveBezierList[0].p0
                    if startPoint == endPoint:
#                        print('Ending. Path already closed')
                        pass
                    else:
#                        print('Ending. Closing path between', startPoint, 'and', endPoint)
                        curveBezierList.append(CubicBezier(startPoint, startPoint, endPoint, endPoint))
#                    print()
                else:
#                    print('Unrecognised command: ',c)
                    pass
        beziergonList.append(Beziergon(curveBezierList))
    return beziergonList


def polygonsFromSVG(filename):
    blist = beziergonsFromSVG(filename)
    polygonList = []
    for b in blist:
        polygonList.append(b.approximateByPolygon().removeZeroLengthLines())
    return polygonList

