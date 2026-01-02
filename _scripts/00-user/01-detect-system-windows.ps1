# Windows System Information Auto Detection Script
# Purpose: Automatic collection of user system information for setup-workspace step
# Usage: powershell -ExecutionPolicy Bypass -File "01-detect-system-windows.ps1"

$ErrorActionPreference = "SilentlyContinue"

# Hash table to store results
$systemInfo = @{
    "os_type" = "windows"
    "timestamp" = (Get-Date -Format "yyyy-MM-ddThh:mm:ssZ")
}

# 1. Detect Python
Write-Host "Checking Python version..." -ForegroundColor Cyan
$pythonVersion = $null
$pythonPath = $null

# Check python command
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($pythonPath) {
    $pythonVersion = python --version 2>&1 | Select-String -Pattern "Python [\d\.]+" | ForEach-Object { $_.Matches[0].Value }
} else {
    # Check python3 command
    $pythonPath = (Get-Command python3 -ErrorAction SilentlyContinue).Source
    if ($pythonPath) {
        $pythonVersion = python3 --version 2>&1 | Select-String -Pattern "Python [\d\.]+" | ForEach-Object { $_.Matches[0].Value }
    }
}

$systemInfo["python"] = @{
    "installed" = $null -ne $pythonVersion
    "version" = if ($pythonVersion) { $pythonVersion } else { "Not installed" }
    "path" = if ($pythonPath) { $pythonPath } else { $null }
}

# 2. Windows OS Information
Write-Host "Checking OS information..." -ForegroundColor Cyan
$os = Get-WmiObject Win32_OperatingSystem
$systemInfo["os"] = @{
    "name" = $os.Caption
    "version" = $os.Version
    "build" = $os.BuildNumber
    "architecture" = $os.OSArchitecture
}

# 3. CPU Information
Write-Host "Checking CPU information..." -ForegroundColor Cyan
$cpu = Get-WmiObject Win32_Processor
$systemInfo["cpu"] = @{
    "name" = $cpu.Name
    "cores" = $cpu.NumberOfCores
    "logical_processors" = $cpu.NumberOfLogicalProcessors
    "speed_ghz" = [math]::Round($cpu.MaxClockSpeed / 1000, 2)
}

# 4. RAM Information
Write-Host "Checking RAM information..." -ForegroundColor Cyan
$computerSystem = Get-WmiObject Win32_ComputerSystem
$totalRAM = [math]::Round($computerSystem.TotalPhysicalMemory / 1GB, 2)
$systemInfo["memory"] = @{
    "total_gb" = $totalRAM
    "available_gb" = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB / 1024, 2)
}

# 5. GPU Information
Write-Host "Checking GPU information..." -ForegroundColor Cyan
$gpus = Get-WmiObject Win32_VideoController
$systemInfo["gpu"] = @{
    "count" = $gpus.Count
    "devices" = @()
}

if ($null -ne $gpus) {
    if ($gpus -is [array]) {
        foreach ($gpu in $gpus) {
            $systemInfo["gpu"]["devices"] += @{
                "name" = $gpu.Name
                "driver_version" = $gpu.DriverVersion
            }
        }
    } else {
        $systemInfo["gpu"]["devices"] += @{
            "name" = $gpus.Name
            "driver_version" = $gpus.DriverVersion
        }
    }
}

# 6. Disk Information (C: drive)
Write-Host "Checking disk information..." -ForegroundColor Cyan
$disk = Get-Volume -DriveLetter C -ErrorAction SilentlyContinue
if ($disk) {
    $systemInfo["disk"] = @{
        "total_gb" = [math]::Round($disk.Size / 1GB, 2)
        "free_gb" = [math]::Round($disk.SizeRemaining / 1GB, 2)
    }
}

# Output in JSON format
Write-Host ""
Write-Host "System information collection completed!" -ForegroundColor Green
Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Collected System Information:" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

# Display in human-readable format
Write-Host ""
Write-Host "OS Information" -ForegroundColor Yellow
Write-Host "   Name: $($systemInfo.os.name)"
Write-Host "   Version: $($systemInfo.os.version) (Build: $($systemInfo.os.build))"
Write-Host "   Architecture: $($systemInfo.os.architecture)"

Write-Host ""
Write-Host "Python" -ForegroundColor Yellow
if ($systemInfo.python.installed) {
    Write-Host "   Status: Installed"
    Write-Host "   Version: $($systemInfo.python.version)"
} else {
    Write-Host "   Status: Not Installed"
}

Write-Host ""
Write-Host "CPU" -ForegroundColor Yellow
Write-Host "   Name: $($systemInfo.cpu.name)"
Write-Host "   Cores: $($systemInfo.cpu.cores) cores / $($systemInfo.cpu.logical_processors) threads"
Write-Host "   Speed: $($systemInfo.cpu.speed_ghz) GHz"

Write-Host ""
Write-Host "RAM" -ForegroundColor Yellow
Write-Host "   Total: $($systemInfo.memory.total_gb) GB"
Write-Host "   Available: $($systemInfo.memory.available_gb) GB"

if ($systemInfo.gpu.count -gt 0) {
    Write-Host ""
    Write-Host "GPU" -ForegroundColor Yellow
    foreach ($device in $systemInfo.gpu.devices) {
        Write-Host "   - $($device.name)"
        Write-Host "     Driver: $($device.driver_version)"
    }
}

if ($systemInfo.disk) {
    Write-Host ""
    Write-Host "Disk (C:)" -ForegroundColor Yellow
    Write-Host "   Total: $($systemInfo.disk.total_gb) GB"
    Write-Host "   Free: $($systemInfo.disk.free_gb) GB"
}

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan

# Also output as JSON (for parsing if needed)
Write-Host ""
Write-Host "JSON format (for parsing):" -ForegroundColor Gray
$systemInfo | ConvertTo-Json -Depth 10 | Write-Host

# Also save to file (optional)
$outputPath = Join-Path $PSScriptRoot "system-info.json"
$systemInfo | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputPath -Encoding UTF8

Write-Host ""
Write-Host "Information saved to: $outputPath" -ForegroundColor Green
