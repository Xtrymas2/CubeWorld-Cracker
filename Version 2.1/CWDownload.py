from urllib.request import urlopen
from zlib import decompress
import os

#Make a new folder for Cube World to go into
INSTALLATION_PATH = 'Cube World\\'
if not os.path.exists(INSTALLATION_PATH):
    os.makedirs(INSTALLATION_PATH)

#This is the official CW download server, and it is where all the files will be downloaded from.
CWDOWNLOAD_AWS = 'http://s3.amazonaws.com/picroma/cwdownload/'
PACKAGE_XML = CWDOWNLOAD_AWS + 'package.xml'

xml = urlopen(PACKAGE_XML).read().decode('UTF-8').split('\n')

#Go through each line in http://s3.amazonaws.com/picroma/cwdownload/package.xml.
#This is what CubeLauncher contacts in order to download the game.
#We'll be finding the name of each one of the files and where they are stored on the server.
for i, line in enumerate(xml):

    #Find the values for 'destination' and 'source'. Destination is the file name and source is location on the server.
    if '<destination>' in line:
        destination = line.split('>')[1].split('<')[0] #The filename to be downloaded to
        source = xml[i+1].split('>')[1].split('<')[0] #AWS file name, this assumes the source will be right after the destination.

        #So many people accidentally tried to use CubeLauncher to run the game that we just won't download it anymore.
        if destination == 'CubeLauncher.exe':
            continue
        
        with open(INSTALLATION_PATH + destination, 'wb') as f:
            #Download, decompress, and save from the CW download server.
            #Each file on the server is stored in a .bin file, which needs to be decompressed by zlib.
            print('Downloading %s' % destination)
            f.write(decompress(urlopen(CWDOWNLOAD_AWS + source).read()))
            
#Cube World requires a db.dat file unique to your machine or else the game will close quickly after starting.
#Changing 6 bytes at 0x5A18D to 0x90 disables this. 
print('Patching Cube.exe')
with open(INSTALLATION_PATH + 'Cube.exe', 'r+b') as f:
    f.seek(0x5A18D)
    f.write(b'\x90' * 6)

#CW needs db.dat to exist
print('Creating a dummy db.dat')
with open(INSTALLATION_PATH + 'db.dat', 'w') as f:
    f.write('PLACEHOLDER000000000000000000000')

input('Installation complete. Use Cube.exe to run the game. Press enter to exit.')    
