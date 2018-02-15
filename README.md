# CubeWorld-Cracker
The newest version of CubeCrack simply installs the game in the same folder as the script/program. This eliminates the complexity of using the old version.

Once the game is installed from the official CW download server (http://s3.amazonaws.com/picroma/cwdownload/), it changes 6 bytes to 0x90 so that the game's DRM features are disabled. The explanation for this is below.

Install.py requires Python 3.X to run. You can download Python 3 from https://www.python.org/

If you do not with to install Python, a py2exe version has been created as well. However, this version requires Administrator permissions to run.

Demo: https://www.youtube.com/watch?v=9htgPoilfZU

# Technical Explanation


## CubeCrack

When you log in normally, the authentication server gives you a valid db.dat for your computer. Db.dat is the file responsible for Cube World's DRM, and if it is invalid, the game shuts down at its soonest opportunity.

When you exit the game normally, it sets a byte at [Cube.exe+0x36B1C8]+0x1A0 to 1. The main loop constantly checks that byte, and if it is 1, it calls PostQuitMessage(), and next loop, it starts actually shutting down.

Cube World opens db.dat and performs some operation on it to see if it's valid for your computer, and then sets the shutdown byte based on the result. The instruction is at 0x5A18D in the executable. Here is the line which sets the byte:

```nasm
...
setz    al
mov     [ebx+1A0h], al  ; Set shutdown byte if db.dat (DRM) was not valid
cmp     [ebp+var_B4], 10h
...
```

CubeCrack removes the instruction which changes the shutdown byte. It won't shut down anymore, since the byte is 0 by default.

