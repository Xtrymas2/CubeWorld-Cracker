# CubeWorld-Cracker
CubeCrack modifies Cube World to run without a valid db.dat

LauncherCrack modifies the launcher to download the game even without an account

CubeLauncher.exe can be installed using https://d1bcl7tdsf48aa.cloudfront.net/download/CubeSetup3.exe

CubeCrack can be used when db.dat is invalid, which will occur if you transfer the game to another computer, or if you force the launcher to download the game without an account.

LauncherCrack can be used to download the game when you don't have an account

Demo: https://www.youtube.com/watch?v=RbCCI6nIMwE

# Technical Explanation



## CubeCrack

-----

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

## LauncherCrack

Cube Launcher is not very sophisticated. There is a comparison and a jump which decides whether your credentials were correct. By changing one byte, LauncherCrack switches a JNE (Jump if not Equal) to JMP (Jump), so it will always download the game, regardless of whether the credentials were correct. Here is the affected code, at 0x14B46 in the executable:

```nasm
...
test    esi, esi
jnz     short loc_41576F ; jmp this for free things
push    es
...
```

The authentication server will not give you a valid db.dat if you download the game like this, so CubeCrack will be needed to bypass it.

