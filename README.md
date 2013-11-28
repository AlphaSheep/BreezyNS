BreezyNS
========

*BreezyNS* is intended to be a simple, general-purpose 2D airflow calculator. It is written in Python with the aim of being able to run with as few external dependencies as possible.

It is currently very much a work in progress.

Technical Stuff
---------------

Breezy is actually an attempt at a computational fluid dynamics (CFD) solver. The work is largely based on Anderson's (1995) and Chung's (2002) books on CFD. 

It loads geometry specified by paths in an SVG file created by a vector graphics program, such as Inkscape. It then generates a mesh using a cartesian boundary meshing scheme, stored as a Quadtree which supports adaptive mesh refinement.

It is intended to solve the Navier-Stokes system of equations which govern the flow of a fluid.

License
-------

BreezyNS is copyright (c) 2013, Brendan Gray under the MIT license.

A copy of the license should have been included with the software. If not, it is available from [http://opensource.org/licenses/MIT].
