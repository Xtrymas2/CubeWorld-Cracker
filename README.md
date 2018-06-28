# CubeWorld-Cracker
Includes CWDownload.py or CWDownload.exe, which downloads Cube World from the update server.

Once the game is installed from the official CW download server (http://s3.amazonaws.com/picroma/cwdownload/), it changes 6 bytes to 0x90 so that the game's DRM features are disabled. The explanation for this is below.

CWDownload.py requires Python 3.X to run. You can download Python 3 from https://www.python.org/

If you do not wish to install Python, A bundled executable version has been created using pyinstaller.

Demo: https://www.youtube.com/watch?v=5ydgRp4FIwI

The Python release is here: https://github.com/ChrisMiuchiz/CubeWorld-Cracker/releases/download/v2.1/CWDownload.py

The bundled executable release is here: https://github.com/ChrisMiuchiz/CubeWorld-Cracker/releases/download/v2.1-exe/CWDownload.exe

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

