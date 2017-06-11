launchern = input('Enter path to launcher: ')

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
    quit()

launcherc = [e for e in launcherc]
launcherc[0x14B46] = 0xEB
launcherc = bytes(launcherc)

try:
    launcherh = open('CubeLauncher_patched.exe', 'wb')
except:
    print('Unable to open CubeLauncher_patched.exe')
    quit()

launcherh.write(launcherc)
launcherh.close()
