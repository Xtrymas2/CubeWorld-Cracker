function Scan-Bytes
{
    param([byte[]]$Source, [byte[]]$Pattern)
    $cadr = 0
    while($cadr -le ($Source.Length - $Pattern.Length))
    {       
        $j = 0;
        while($j -lt $Pattern.Length -and $Source[$cadr + $j] -eq $Pattern[$j])
        {
            #Write-Output $j
            $j += 1
            if($j -eq $Pattern.Length)
            {
                return $cadr
            }

        }
        $cadr += 1
    }
    return -1
}
$CPattern = [byte[]](0x85, 0xC0,                               #test eax, eax
                     0x0F, 0x94, 0xC0,                         #setz al
                     0x88, 0x83, 0xA0, 0x01, 0x00, 0x00,       #mov [ebx+1A0], al
                     0x83, 0xBD, 0x4C, 0xFF, 0xFF, 0xFF, 0x10, #cmp dword ptr [ebp-B4], 10
                     0xC6, 0x45, 0xFC, 0x3D)                   #mov byte prt [ebp-04], 3D

$CPatch = [byte[]](0x90, 0x90, 0x90, 0x90, 0x90, 0x90)

Write-Output "EXAMPLE: C:\Program Files (x86)\Cube World\Cube.exe"
$CPath = Read-Host -Prompt "Enter path to Cube.exe"

If((Test-Path $CPath) -eq $False)
{
    Write-Host "Could not find file at path: '$CPath'`r`nPress any key to continue..."
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
    Exit
}

$CBytes = [System.IO.File]::ReadAllBytes($CPath)
$Offset = Scan-Bytes -Source $CBytes -Pattern $CPattern

If($Offset -eq -1)
{
    Write-Host "Failed to find pattern, unable to crack!`r`nPress any key to continue..."
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
    Exit
}

[Array]::Copy($CPatch, 0, $CBytes, $Offset + 5, 6)
$Directory = Split-Path -Path $CPath
[System.IO.File]::WriteAllBytes($Directory + "\cube.patched.exe", $CBytes)
[System.IO.File]::WriteAllText($Directory + "\db.dat", "NOTAREALDRMKEY000000000000000000")
Write-Host "Done."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
