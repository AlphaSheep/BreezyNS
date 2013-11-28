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



class ShearTensor ():
    def __init__(self):
        self.tensor = [[0,0],[0,0]]
        
    def calculate(self):
        # Apply a Newtonion model, using finite differences for the spacial derivatives
        return self
    
    def getElem(self, i, j):
        return self.tensor[i][j]
    
    def xx(self):
        return self.tensor[0][0]
    
    def xy(self):
        return self.tensor[0][1]
        
    def yx(self):
        return self.tensor[1][0]
    
    def yy(self):
        return self.tensor[1][1]
        
        