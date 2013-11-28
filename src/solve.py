'''
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

