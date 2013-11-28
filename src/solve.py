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

from pycfdsolver.basicvector import Vector
from pycfdsolver.navierstokes import SolutionVector, FluxVector
from pycfdsolver.stateequation import pressure


rho = 1.225
vel = Vector(2).set(500,0)
pressure = 101325
gamma = 1.4
energy = (1/(gamma-1))*pressure/rho + vel.sumOfSquares()/2

s = SolutionVector()
s.set(rho, vel, energy)

print ("Solution:",s)
print ()

print("Density:",s.getDensity())
print("Velocity:",s.getVelocity())
print("Energy:",s.getTotalEnergy())
print("Pressure:",s.getPressure())
print ()


F = FluxVector(0).calculate(s)
G = FluxVector(1).calculate(s)

print ("Flux X:",F)
print ("Flux Y:",G)
print()

H = F + G

print ("Flux X:",F)
print ("Flux Y:",G)
print ("F+G:",H)

