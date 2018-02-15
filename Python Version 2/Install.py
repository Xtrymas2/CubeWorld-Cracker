from urllib.request import urlopen
from zlib import decompress

#This is the official CW download server, and it is where all the files will be downloaded from.
CWDOWNLOAD_AWS = 'http://s3.amazonaws.com/picroma/cwdownload/'

xml = urlopen(CWDOWNLOAD_AWS + 'package.xml').read().decode('UTF-8')
lines = xml.split('\n')
for i, line in enumerate(lines):
    if '<destination>' in line:
        destination = line.split('>')[1].split('<')[0] #The filename to be downloaded to
        source = lines[i+1].split('>')[1].split('<')[0] #AWS file name
        with open(destination, 'wb') as f:
            #Download, decompress, and save from the CW download server
            print('Downloading %s' % destination)
            f.write(decompress(urlopen(CWDOWNLOAD_AWS + source).read()))
            
#CW needs db.dat to exist            
with open('db.dat', 'w') as f:
    f.write('PLACEHOLDER000000000000000000000')

#Patch some bytes with 0x90 to disable DRM features
print('Patching Cube.exe')
with open('Cube.exe', 'rb') as f:
    cubeData = [x for x in f.read()]   
with open('Cube.exe', 'wb') as f:
    cubeData[0x5A18D:0x5A193] = [0x90]*6
    f.write(bytes(cubeData))
        
input('Installation complete. Use Cube.exe to run the game. Press enter to exit.')    
    
