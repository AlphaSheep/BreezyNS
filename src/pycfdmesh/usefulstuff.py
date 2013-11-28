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



Created on 04 Sep 2013

@author: AlphanumericSheepPig
'''




def floatRange(start , stop= None, step = 1.0):
    ''' Generator object to mimic behaviour of range, but with floats. '''
    if stop == None:
        startPoint = 0.0
        stopPoint = start
    else:
        startPoint = start
        stopPoint = stop
    current = 0
    value = startPoint + current*step
    while value<stopPoint:
        yield startPoint + current*step
        current += 1
        value = startPoint + current*step


def saveFile(filename,contents, path = ''):
    if len(path) > 0 and not path[-1] in ['\\','/'] :
        path += '/'         
    try:
        file = open(path + filename, 'w')
        for line in contents:
            file.write(line+'\n')
        file.close()
        return True
    except IOError:
        print ('Encountered error while trying to save file '+filename)
        return False
    
    
    