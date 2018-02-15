# Powershell Patch

Powershell is pretty neato, however Bill over at Microsoft decided to be a little anal about the execution of Powershell scripts, so if you've never used Powershell scripts this will most likely effect you, otherwise you're probably good.

Powershell by default does not allow execution of scripts. So to enable the execution of Powershell scripts you have 2 choices.

 - Use Unrestricted mode and download the file.
 - Use RemoteSigned mode and copy the file contents of the script into a file you created locally.
 
Unrestricted mode, as the name says, allows any script to run, the most potentially dangerous of the lot.
However RemoteSigned only requires scripts that are downloaded to be signed, all locally created scripts can be run without certificates.

To apply either of these modes, simply open PowerShell as Administrator and enter either of these commands for what you want.

```sh
Set-ExecutionPolicy RemoteSigned
Set-ExecutionPolicy Unrestricted
```

After that all you have to do is double click on the script or right click 'Open with PowerShell'. And of course you can always revert back to not allowing any PowerShell scripts to be run by entering:
```sh
Set-ExecutionPolicy Restricted
```

Honestly pretty shitty policy considering executables can still execute freely, anywho, enjoy!
