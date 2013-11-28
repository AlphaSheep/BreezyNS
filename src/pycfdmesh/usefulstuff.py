'''
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
    
    
    