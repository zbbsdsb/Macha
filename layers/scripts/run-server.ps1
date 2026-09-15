#requires -Version 5.1
# ---------------------------------------------------------------------------
# run-server.ps1 - start / manage the Macha Paper server (M0).
#
# Purpose:
#   * First run: download the Paper jar (if missing) -> verify sha256 ->
#     ensure eula/server.properties -> start the server.
#   * Managed mode: boot -> wait "Done" -> wait .stop flag -> graceful RCON stop.
#   * Server home is pinned at layers/run/minecraft/ (gitignored by layers/.gitignore).
#
# Boundary: this script only boots/stops the server and manages eula/properties.
# Protocol/plugin logic does not live here.
#
# JDK (M0-D): Paper 26.2 needs Java 25; machine default PATH/JAVA_HOME is JDK 21.
# Resolution order: $env:MACHA_JDK25 -> probe "$env:USERPROFILE\.gradle\jdks\*\bin\java.exe"
# where `java -version` matches "25" -> common install dirs -> throw with guidance.
# No username is hardcoded.
#
# server.properties (M0-C): managed keys are updated/backfilled but existing
# values of other keys (e.g. difficulty) are preserved; the file is only written
# in full when it does not exist.
#
# Managed stop (M0-B): on .stop we send the `stop` command over RCON (enabled in
# server.properties) so the server shuts down gracefully ("Stopping server" /
# "Saving players"). Force-kill only as a fallback.
#
# Usage:
#   .\run-server.ps1                      # foreground, interactive ("stop" to quit)
#   .\run-server.ps1 -Managed             # managed: boot -> Done -> wait .stop -> RCON stop
#   .\run-server.ps1 -Managed -ResetConfig# force rewrite server.properties fresh
#   .\run-server.ps1 -SkipDownload        # skip network (use when jar already present)
# ---------------------------------------------------------------------------
[CmdletBinding()]
param(
    [switch]$Managed,
    [switch]$SkipDownload,
    [switch]$ResetConfig
)

$ErrorActionPreference = 'Stop'

# ---- constants (match version locks in research/plans/minecraft-layer/03 §2 / 00 §C.1) ----
$PaperVersion = '26.2'
$PaperBuild   = 123
# sha256 is the REAL lock; the on-disk filename is just paper-server.jar (M0-E).
$PaperSha256  = '7b7b3b43c009103e1971a0576c26f655a7dd9b56a0a2a4438e352c03a7fecd08'
$ServerJvm    = @('-Xms1G', '-Xmx2G', '-jar', 'paper-server.jar', 'nogui')

# ---- paths ----
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LayersDir = Split-Path -Parent $ScriptDir              # layers/
$RunDir    = Join-Path $LayersDir 'run'
$ServerDir = Join-Path $RunDir 'minecraft'              # layers/run/minecraft/  server home
$JarPath   = Join-Path $ServerDir 'paper-server.jar'
$ConsoleLog= Join-Path $ServerDir 'console.log'
$ConsoleErr= Join-Path $ServerDir 'console.err'
$StopFlag  = Join-Path $ServerDir '.stop'
$ReadyFlag = Join-Path $ServerDir '.ready'
$PidFile   = Join-Path $ServerDir '.pid'

# RCON (M0-B) resolved by Ensure-Config from server.properties
$script:RCONPort     = 25575
$script:RCONPassword = ''

function Write-Step($msg) { Write-Host "[run-server] $msg" }

# ---- JDK 25 resolution (M0-D) ----
$script:JDKPath = $null

# Probe a java.exe's version string via .NET process (java writes to stderr; a naive
# `& $j -version 2>&1` can be surfaced as a NativeCommandError and, under
# $ErrorActionPreference='Stop', abort the script — so capture stderr structurally).
function Get-JavaVersion([string]$java) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $java
    $psi.Arguments = '-version'
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true
    try {
        $proc = [System.Diagnostics.Process]::Start($psi)
        $err = $proc.StandardError.ReadToEnd()
        $proc.WaitForExit()
        return $err
    } catch {
        return ''
    }
}

function Resolve-Jdk {
    if ($script:JDKPath) { return $script:JDKPath }
    $candidates = New-Object System.Collections.Generic.List[string]

    if ($env:MACHA_JDK25) { $candidates.Add($env:MACHA_JDK25) }
    if ($env:USERPROFILE) {
        $glob = Join-Path $env:USERPROFILE '.gradle\jdks'
        if (Test-Path $glob) {
            Get-ChildItem -Path $glob -Directory -ErrorAction SilentlyContinue |
                ForEach-Object { $j = Join-Path $_.FullName 'bin\java.exe'; if (Test-Path $j) { $candidates.Add($j) } }
        }
    }
    $commonRoots = @(
        (Join-Path $env:ProgramFiles 'Eclipse Adoptium'),
        (Join-Path $env:ProgramFiles 'Java'),
        (Join-Path $env:ProgramFiles 'Microsoft'),
        (Join-Path ${env:ProgramFiles(x86)} 'Java')
    )
    foreach ($root in $commonRoots) {
        if ($root -and (Test-Path $root)) {
            Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue |
                ForEach-Object { $j = Join-Path $_.FullName 'bin\java.exe'; if (Test-Path $j) { $candidates.Add($j) } }
        }
    }

    foreach ($j in $candidates) {
        $ver = Get-JavaVersion -java $j
        if ($ver -match 'version "25') {
            $script:JDKPath = $j
            Write-Step "JDK 25 resolved: $j"
            return $j
        }
    }

    throw @"
No Java 25 found. Paper 26.2 requires Java 25 (machine default PATH is JDK 21).
  - Set `$env:MACHA_JDK25 to a JDK 25 java.exe, or
  - install Temurin 25 (e.g. under `$env:ProgramFiles\Eclipse Adoptium), or
  - place a JDK 25 under `$env:USERPROFILE\.gradle\jdks\<name>\bin\java.exe.
"@
}

# ---- 1) ensure jar: download + sha256 check ----
function Ensure-Jar {
    if (-not (Test-Path $JarPath)) {
        if ($SkipDownload) {
            throw "jar missing and download skipped: $JarPath (drop -SkipDownload or run with network first)"
        }
        Write-Step "Downloading Paper $PaperVersion build $PaperBuild ..."
        $api    = "https://fill.papermc.io/v3/projects/paper/versions/$PaperVersion/builds"
        $builds = Invoke-RestMethod -Uri $api
        $target = $builds | Where-Object { $_.id -eq $PaperBuild }
        if (-not $target) {
            throw "Paper $PaperVersion has no build $PaperBuild (queried $api)"
        }
        $url = $target.downloads.'server:default'.url
        Invoke-WebRequest -Uri $url -OutFile $JarPath
    } else {
        Write-Step "jar already present: $JarPath"
    }

    $hash = (Get-FileHash -Algorithm SHA256 -Path $JarPath).Hash.ToLowerInvariant()
    if ($hash -ne $PaperSha256) {
        Remove-Item -Force $JarPath
        throw "sha256 mismatch for $PaperVersion-$PaperBuild; deleted $JarPath.`n  expected $PaperSha256`n  got      $hash"
    }
    Write-Step "jar checksum ok: $PaperVersion-$PaperBuild sha256=$hash"
}

# ---- RCON client (M0-B) ----
function New-RconPacket([int]$Id, [int]$Type, [string]$Body) {
    $bodyBytes = [System.Text.Encoding]::ASCII.GetBytes($Body)
    $ms = New-Object System.IO.MemoryStream
    $bw = New-Object System.IO.BinaryWriter($ms)
    $length = 4 + 4 + $bodyBytes.Length + 2
    $bw.Write([BitConverter]::GetBytes([int]$length))
    $bw.Write([BitConverter]::GetBytes([int]$Id))
    $bw.Write([BitConverter]::GetBytes([int]$Type))
    $bw.Write($bodyBytes)
    $bw.Write([byte[]](0, 0))
    $bw.Flush()
    return $ms.ToArray()
}

function Read-RconPacket($stream) {
    $lb = New-Object byte[] 4
    $got = $stream.Read($lb, 0, 4)
    if ($got -lt 4) { return $null }
    $len = [BitConverter]::ToInt32($lb, 0)
    $buf = New-Object byte[] $len
    $read = 0
    while ($read -lt $len) {
        $n = $stream.Read($buf, $read, $len - $read)
        if ($n -le 0) { break }
        $read += $n
    }
    return @{
        Id   = [BitConverter]::ToInt32($buf, 0)
        Type = [BitConverter]::ToInt32($buf, 4)
        Body = [System.Text.Encoding]::ASCII.GetString($buf, 8, $len - 8 - 2)
    }
}

function Send-RconCommand {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Password,
        [Parameter(Mandatory)][int]$Port,
        [Parameter(Mandatory)][string]$Command
    )
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $client.Connect('127.0.0.1', $Port)
        $stream = $client.GetStream()

        $auth = New-RconPacket -Id 7 -Type 3 -Body $Password
        $stream.Write($auth, 0, $auth.Length); $stream.Flush()
        $resp = Read-RconPacket $stream
        if (-not $resp -or $resp.Type -ne 2) {
            throw "RCON auth failed (type=$($resp.Type))"
        }

        $cmdPkt = New-RconPacket -Id 8 -Type 2 -Body $Command
        $stream.Write($cmdPkt, 0, $cmdPkt.Length); $stream.Flush()
        return $true
    } finally {
        $client.Close()
    }
}

# ---- 2) eula / server.properties ----
# NOTE: Paper's EULA parser requires line 1 to be exactly `eula=true`. A UTF-8 BOM
# (EF BB BF) corrupts the first line and Paper refuses a genuinely-agreed eula.txt.
# Always write UTF-8 WITHOUT BOM (re-verify: build 123 rejects BOM'd eula).
function New-RconPassword {
    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    $rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
    $b = New-Object byte[] 24
    $rng.GetBytes($b)
    $sb = New-Object System.Text.StringBuilder
    foreach ($byte in $b) { [void]$sb.Append($chars[[int]$byte % $chars.Length]) }
    $rng.Dispose()
    return $sb.ToString()
}

function Ensure-Config {
    $eula = Join-Path $ServerDir 'eula.txt'
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($eula, 'eula=true', $utf8NoBom)

    # Keys the script owns (M0-B enable-rcon + M0-C minimal set). Everything else in an
    # existing server.properties is preserved untouched (e.g. difficulty).
    $managed = [ordered]@{
        'online-mode'      = 'false'
        'level-type'       = 'flat'
        'spawn-protection' = '0'
        'view-distance'    = '6'
        'level-name'       = 'macha_world'
        'enable-rcon'      = 'true'
        'rcon.port'        = '25575'
    }
    $script:RCONPort = [int]$managed['rcon.port']

    $sp = Join-Path $ServerDir 'server.properties'
    $lines = New-Object System.Collections.Generic.List[string]
    if ((Test-Path $sp) -and -not $ResetConfig) {
        foreach ($line in (Get-Content $sp)) {
            if ($line -notmatch '^\s*#') { $lines.Add($line) }
        }
    }

    foreach ($k in $managed.Keys) {
        $idx = -1
        for ($i = 0; $i -lt $lines.Count; $i++) {
            if ($lines[$i] -match "^$([regex]::Escape($k))=") { $idx = $i; break }
        }
        if ($idx -ge 0) { $lines[$idx] = "$k=$($managed[$k])" } else { $lines.Add("$k=$($managed[$k])") }
    }

    $pwIdx = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^rcon\.password=') { $pwIdx = $i; break }
    }
    $curPw = if ($pwIdx -ge 0) { $lines[$pwIdx] -replace '^rcon\.password=', '' } else { '' }
    if ([string]::IsNullOrEmpty($curPw)) {
        $curPw = New-RconPassword
        if ($pwIdx -ge 0) { $lines[$pwIdx] = "rcon.password=$curPw" } else { $lines.Add("rcon.password=$curPw") }
    }
    $script:RCONPassword = $curPw

    [System.IO.File]::WriteAllLines($sp, $lines, $utf8NoBom)
    Write-Step "server.properties ensured (managed keys: $($managed.Keys -join ', '), rcon.port=$script:RCONPort)"
}

# ---- 3) launch ----
function Start-Foreground {
    $jdk = Resolve-Jdk
    Write-Step "JDK: $(& $jdk -version 2>&1 | Select-Object -First 1)"
    Write-Step "Server dir: $ServerDir   (type stop to quit gracefully; console also via RCON)"
    Push-Location $ServerDir
    try {
        & $jdk @ServerJvm
    } finally {
        Pop-Location
    }
}

function Start-Managed {
    # Automated boot/stop for CI: launch java (Start-Process drains stdout -> console.log),
    # wait for "Done (" to write .ready, then wait for the .stop flag and issue an RCON
    # "stop" for a graceful shutdown. Clean up .ready/.stop/.pid on exit (M0-F).
    $jdk = Resolve-Jdk
    Remove-Item $ReadyFlag,$StopFlag,$PidFile -ErrorAction SilentlyContinue
    Remove-Item $ConsoleLog,$ConsoleErr -ErrorAction SilentlyContinue

    Write-Step "Managed boot (stdout -> $ConsoleLog) ..."
    $proc = Start-Process -FilePath $jdk -ArgumentList $ServerJvm -WorkingDirectory $ServerDir `
        -RedirectStandardOutput $ConsoleLog -RedirectStandardError $ConsoleErr `
        -WindowStyle Hidden -PassThru
    Set-Content -Path $PidFile -Value $proc.Id

    Write-Step "Waiting for server Done ..."
    $deadline = (Get-Date).AddMinutes(5)
    while (-not (Test-Path $ReadyFlag)) {
        if ($proc.HasExited) { throw "server exited early, exit=$($proc.ExitCode); see $ConsoleLog" }
        if ((Get-Date) -gt $deadline) { throw "timed out waiting for Done (5 min); see $ConsoleLog" }
        Start-Sleep -Milliseconds 500
        if ((Get-Content $ConsoleLog -Raw -ErrorAction SilentlyContinue) -match 'Done \(') {
            '' | Set-Content $ReadyFlag -NoNewline
        }
    }
    Write-Step "Done seen. Waiting for .stop flag -> RCON stop ..."

    while (-not (Test-Path $StopFlag)) {
        if ($proc.HasExited) { break }
        Start-Sleep -Milliseconds 500
    }

    if (-not $proc.HasExited) {
        Write-Step "Stop requested; sending RCON 'stop' for graceful shutdown ..."
        $stopped = $false
        try {
            $stopped = Send-RconCommand -Password $script:RCONPassword -Port $script:RCONPort -Command 'stop'
        } catch {
            Write-Warning "RCON stop failed: $_"
        }
        if ($stopped) {
            if (-not $proc.WaitForExit(60000)) {
                Write-Warning "server did not exit within 60s of RCON stop; forcing terminate"
                Stop-Process -Id $proc.Id -Force
            }
        } else {
            Write-Warning "RCON unavailable; falling back to force terminate (see README 'hard-stop risk')"
            if (-not $proc.HasExited) { Stop-Process -Id $proc.Id -Force }
        }
        $proc.WaitForExit(10000) | Out-Null
    }

    Remove-Item $ReadyFlag,$StopFlag,$PidFile -ErrorAction SilentlyContinue
    Write-Step "Server stopped. Cleaned up .ready/.stop/.pid (M0-F)"
}

# ---- main ----
New-Item -ItemType Directory -Force -Path $ServerDir | Out-Null
Ensure-Jar
Ensure-Config
Resolve-Jdk | Out-Null   # fail fast with guidance if Java 25 is missing
if ($Managed) { Start-Managed } else { Start-Foreground }