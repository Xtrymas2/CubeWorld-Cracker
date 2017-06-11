launchern = input('EXAMPLE: C:\\Program Files (x86)\\Cube World\\CubeLauncher.exe\nEnter path to launcher: ')

try:
    launcherh = open(launchern, 'rb')
except:
    print('Unable to open', launchern)

launcherc = launcherh.read()
launcherh.close()

if len(launcherc) != 163840:
    print('This is not the latest version of the launcher.')
    print('You can download it from:')
    print('https://d1bcl7tdsf48aa.cloudfront.net/download/CubeSetup3.exe')
    input()
    quit()

launcherc = [e for e in launcherc]
launcherc[0x14B46] = 0xEB #turn conditional jump into jmp
launcherc = bytes(launcherc)
outfilename = 'CubeLauncher_patched.exe'

try:
    launcherh = open(outfilename, 'wb')
except:
    print('Unable to open', outfilename)
    input()
    quit()

launcherh.write(launcherc)
launcherh.close()
print(outfilename, 'has been created')
input()
