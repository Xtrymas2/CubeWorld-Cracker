from urllib.request import urlopen
from zlib import decompress
import os
import xml.etree.ElementTree as ElementTree

#Make a new folder for Cube World to go into
INSTALLATION_PATH = 'Cube World'
if not os.path.exists(INSTALLATION_PATH):
    os.makedirs(INSTALLATION_PATH)

#This is the official CW download server, and it is where all the files will be downloaded from.
CWDOWNLOAD_AWS = 'http://s3.amazonaws.com/picroma/cwdownload/'
PACKAGE_XML = CWDOWNLOAD_AWS + 'package.xml'

XML_data = urlopen(PACKAGE_XML).read().decode('UTF-8')
package = ElementTree.fromstring(XML_data)

#Go through each file listed at http://s3.amazonaws.com/picroma/cwdownload/package.xml.
#This is what CubeLauncher contacts in order to download the game.
#We'll be finding the name of each one of the files and where they are stored on the server.
for file in package.iter('file'):
    
    #Find the values for 'destination' and 'source'. Destination is the file name and source is location on the server.
    destination = file.find('destination').text
    source = file.find('source').text

    #So many people accidentally tried to use CubeLauncher to run the game that we just won't download it anymore.
    if destination == 'CubeLauncher.exe':
        continue
    
    with open(os.path.join(INSTALLATION_PATH, destination), 'wb') as f:
            #Download, decompress, and save from the CW download server.
            #Each file on the server is stored in a .bin file, which needs to be decompressed by zlib.
            print('Downloading %s' % destination)
            compressed_data = urlopen(CWDOWNLOAD_AWS + source).read()
            raw_data = bytearray(decompress(compressed_data))
            
            #Cube World requires a db.dat file unique to your machine or else the game will close quickly after starting.
            #Changing 6 bytes at 0x5A18D in Cube.exe to 0x90 disables this.
            #raw_data has been converted into a bytearray to support this operation.
            #This operation is now being done prior to saving the game because antivirus programs didn't like modifying Cube.exe after being saved.
            if destination == 'Cube.exe':
                print('Patching Cube.exe')
                raw_data[0x5A18D : 0x5A18D + 0x6] = b'\x90' * 6
                
            f.write(raw_data)

#CW needs db.dat to exist
print('Creating a dummy db.dat')
with open(os.path.join(INSTALLATION_PATH, 'db.dat'), 'w') as f:
    f.write('PLACEHOLDER000000000000000000000')

input('Installation complete. Use Cube.exe to run the game. Press enter to exit.')    
