#requires -Version 5.1
# ---------------------------------------------------------------------------
# run-server.ps1 - start / manage the Macha Paper server (M0).
#
# Purpose:
#   1. First run: download the Paper jar (if missing) -> verify sha256 ->
#      write eula/server.properties -> start the server.
#   2. Server home is pinned at layers/run/minecraft/ (excluded from git by
#      layers/.gitignore's run/ entry).
#   3. The machine default PATH/JAVA_HOME point to JDK 21, but Paper 26.2
#      requires Java 25 -> launch must explicitly use the Temurin 25 java.exe
#      below (verified 25.0.4.1).
#
# Usage:
#   .\run-server.ps1                      # foreground, interactive ("stop" to quit)
#   .\run-server.ps1 -Managed             # managed: boot -> wait Done -> wait .stop flag -> graceful stop
#   .\run-server.ps1 -SkipDownload        # skip network (use when jar already present)
#
# Boundary: this script only boots/stops the server and writes eula/properties.
# Protocol/plugin logic does not live here.
# ---------------------------------------------------------------------------
[CmdletBinding()]
param(
    [switch]$Managed,
    [switch]$SkipDownload
)

$ErrorActionPreference = 'Stop'

# ---- constants (match version locks in research/plans/minecraft-layer/03 §2) ----
$PaperVersion = '26.2'
$PaperBuild   = 123
$PaperSha256  = '7b7b3b43c009103e1971a0576c26f655a7dd9b56a0a2a4438e352c03a7fecd08'
$Jdk25        = 'C:\Users\chkev\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2\bin\java.exe'
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

function Write-Step($msg) { Write-Host "[run-server] $msg" }

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

# ---- 2) eula / server.properties ----
# NOTE: Paper's EULA parser reads line 1 and requires exactly `eula=true`.
# PS 5.1 Set-Content can emit a UTF-8 BOM (`EF BB BF`), which corrupts the first
# line and makes Paper reject a genuinely-agreed eula.txt. Always write UTF-8
# WITHOUT BOM here (verified: build 123 refuses BOM'd eula, then crashes or loops
# "You need to agree to the EULA"). Rewriting every boot also clears stale files.
function Ensure-Config {
    $eula = Join-Path $ServerDir 'eula.txt'
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($eula, 'eula=true', $utf8NoBom)

    $sp = Join-Path $ServerDir 'server.properties'
    $props = @(
        'online-mode=false',
        'level-type=flat',
        'spawn-protection=0',
        'view-distance=6',
        'level-name=macha_world'
    ) -join "`n"
    [System.IO.File]::WriteAllText($sp, $props, $utf8NoBom)
}

# ---- 3) launch ----
function Start-Foreground {
    Write-Step "Foreground boot (JDK: $(& $Jdk25 -version 2>&1 | Out-String | Select-Object -First 1))"
    Write-Step "Server dir: $ServerDir   (type stop to quit gracefully)"
    Push-Location $ServerDir
    try {
        & $Jdk25 @ServerJvm
    } finally {
        Pop-Location
    }
}

function Start-Managed {
    # Automated boot/stop for CI: launch java with stdout -> console.log (Start-Process
    # internally drains stdout so java never blocks), wait for "Done (" to write .ready,
    # then wait for the .stop flag and terminate the server.
    #
    # Note: we intentionally do NOT redirect stdin here (graceful "stop" is unavailable to
    # an automated launcher), so managed stop is a process terminate, not the "stop" command.
    # Use the interactive foreground mode for a graceful, human-supervised shutdown.
    Remove-Item $ReadyFlag -ErrorAction SilentlyContinue
    Remove-Item $StopFlag  -ErrorAction SilentlyContinue
    Remove-Item $ConsoleLog,$ConsoleErr -ErrorAction SilentlyContinue

    Write-Step "Managed boot (stdout -> $ConsoleLog) ..."
    $proc = Start-Process -FilePath $Jdk25 -ArgumentList $ServerJvm -WorkingDirectory $ServerDir `
        -RedirectStandardOutput $ConsoleLog -RedirectStandardError $ConsoleErr `
        -WindowStyle Hidden -PassThru
    Set-Content -Path (Join-Path $ServerDir '.pid') -Value $proc.Id

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
    Write-Step "Done seen. Waiting for .stop flag -> terminate ..."

    while (-not (Test-Path $StopFlag)) {
        if ($proc.HasExited) { break }
        Start-Sleep -Milliseconds 500
    }

    Write-Step "Stop requested; terminating server process ..."
    if (-not $proc.HasExited) { Stop-Process -Id $proc.Id -Force }
    $proc.WaitForExit(30000) | Out-Null
    Remove-Item (Join-Path $ServerDir '.pid') -ErrorAction SilentlyContinue
    Write-Step "Server stopped."
}

# ---- main ----
New-Item -ItemType Directory -Force -Path $ServerDir | Out-Null
Ensure-Jar
Ensure-Config
if (-not (Test-Path $Jdk25)) {
    throw "JDK 25 not found: $Jdk25 (Paper $PaperVersion needs Java 25; default PATH is JDK 21)"
}
if ($Managed) { Start-Managed } else { Start-Foreground }