'''
This file is a part of BreezyNS - a simple, general-purpose 2D airflow calculator.

BreezyNS is copyright (c) 2013, Brendan Gray

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

import copy


class Vector():
    '''
    A simple generic vector class with some useful methods
    '''
    def __init__(self, size):
        self.vect = []
        for i in range(size):
            self.vect.append(0.0)
    
    def set(self, *content):
        if len(self.vect) == len(content):
            for i in range(len(content)):
                self.vect[i] = (content[i])
        else:
            vectorLengthMismatch = "Cannot assign {:d} elements to a vector of length {:d}".format(len(content), len(self.vect))
            raise Exception(vectorLengthMismatch)
        return self
        
    def x(self):
        if len(self.vect) == 2:
            return self.vect[0]
        else:
            raise Exception("There's probably a mistake somewhere because only vectors of length 2 should have x and y components.")
        
    def y(self):
        if len(self.vect) == 2:
            return self.vect[1]
        else:
            raise Exception("There's probably a mistake somewhere because only vectors of length 2 should have x and y components.")
    
    def setElem(self, elem, value):
        self.vect[elem] = value

    def getElem(self, elem):
        return self.vect[elem]
    
    def sumOfSquares(self):
        res = 0
        for e in self.vect:
            res += e*e
        return res
    
    def __add__(self, other):
        if len(self.vect) == len(other.vect):
            
            # If this method was inherited by another class, we need to be very careful that the returned vector is 
            # the same type as the originals, so that it can still access methods provided by the child class.
            # For this reason, we avoid explicitly creating a new instance of Vector, but rather perform a deepcopy of 
            # one of the originals. I'm not really sure that this is the best way of doing this...
            
            res = copy.deepcopy(self)
            for i in range(len(self.vect)):
                res.vect[i] += other.vect[i]
            return res  
                
        else:
            vectorLengthMismatch = "Cannot add a vector of length {:d} to a vector of length {:d}".format(len(self.vect), len(other.vect))
            raise Exception(vectorLengthMismatch)


    def __str__(self):
        str = "( "
        for i in range(len(self.vect)-1):
            str += "{:g}, ".format(self.vect[i])
        str += "{:g} )".format(self.vect[-1])
        return str
    