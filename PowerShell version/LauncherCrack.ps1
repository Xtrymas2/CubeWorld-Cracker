Write-Output "EXAMPLE: C:\Program Files (x86)\Cube World\CubeLauncher.exe"
$CPath = Read-Host -Prompt "Enter path to CubeLauncher.exe"

If((Test-Path $CPath) -eq $False)
{
    Write-Host "Could not find file at path: '$CPath'`r`nPress any key to continue..."
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
    Exit
}

$CBytes = [System.IO.File]::ReadAllBytes($CPath)

If($CBytes.Length -ne 163840)
{
    Write-Host "This is not the latest version of the launcher.`r`nYou can download it from:`r`nhttps://d1bcl7tdsf48aa.cloudfront.net/download/CubeSetup3.exe`r`nPress any key to continue..."
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
    Exit
}
$CBytes[0x14B46] = 0xEB
$Directory = Split-Path -Path $CPath
[System.IO.File]::WriteAllBytes($Directory + "\CubeLauncher.patched.exe", $CBytes)
Write-Host "Done."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
