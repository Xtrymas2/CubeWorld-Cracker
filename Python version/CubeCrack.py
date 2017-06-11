def AOBScan(AOB, contents, desiredresult): #Returns address at which the AOB is located.
    resultnumber = 0
    address = 0
    while address <= len(contents)-len(AOB):
        j=0
        while j<len(AOB) and contents[address+j]==AOB[j]:
            j+=1
            if j == len(AOB):
                resultnumber += 1
                if resultnumber == desiredresult:
                    return address
        address += 1
    return -1

DRMbytes = [
            0x85, 0xC0,                               #test eax, eax
            0x0F, 0x94, 0xC0,                         #setz al
            0x88, 0x83, 0xA0, 0x01, 0x00, 0x00,       #mov [ebx+1A0], al
            0x83, 0xBD, 0x4C, 0xFF, 0xFF, 0xFF, 0x10, #cmp dword ptr [ebp-B4], 10
            0xC6, 0x45, 0xFC, 0x3D,                   #mov byte prt [ebp-04], 3D
            ]
patchbytes =[
            0x85, 0xC0,                               #test eax, eax
            0x0F, 0x94, 0xC0,                         #setz al
            0x90, 0x90, 0x90, 0x90, 0x90, 0x90,       #nop nop nop nop nop nop
            0x83, 0xBD, 0x4C, 0xFF, 0xFF, 0xFF, 0x10, #cmp dword ptr [ebp-B4], 10
            0xC6, 0x45, 0xFC, 0x3D,                   #mov byte prt [ebp-04], 3D
            ]

cubeFile = input('EXAMPLE: C:\\Program Files (x86)\\Cube World\\CubeLauncher.exe\nEnter path to Cube.exe: ')
try:
    cubeh = open(cubeFile, 'rb')
except:
    print('Unable to open', cubeFile)
    input()
    quit()
cubec = cubeh.read()
cubeh.close()
loc = AOBScan(DRMbytes, cubec, 1)

if loc == -1:
    print('Unable to crack.')
    input()
    quit()

cubec = [e for e in cubec]
cubec[loc:loc+len(DRMbytes)] = patchbytes
cubec = bytes(cubec)

outname = 'Cube_patched.exe'
try:
    outh = open(outname, 'wb')
except:
    print('Unable to open', outname)
    input()
    quit()

try:
    outdbh = open('db.dat', 'w')
except:
    print('Unable to open db.dat')
    input()
    quit()

#A db.dat still has to exist.
outdbh.write('NOTAREALDRMKEY000000000000000000')
outdbh.close()

outh.write(cubec)
outh.close()

print(outname, 'has been created\ndb.dat has been created')
input()
