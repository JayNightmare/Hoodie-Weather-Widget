# Hoodie Weather Widget - Build System (PowerShell)
# Enhanced build script with better error handling and user experience

param(
    [switch]$PortableOnly,
    [switch]$InstallerOnly,
    [switch]$NoBuild,
    [switch]$Help
)

# Color functions for better output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✅ $Message" "Green"
}

function Write-Error {
    param([string]$Message) 
    Write-ColorOutput "❌ $Message" "Red"
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ️ $Message" "Cyan"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠️ $Message" "Yellow"
}

function Show-Help {
    Write-ColorOutput "🧥 Hoodie Weather Widget - Build System" "Yellow"
    Write-ColorOutput "=" * 50 "Yellow"
    Write-Host ""
    Write-Host "Usage: .\build.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -PortableOnly    Build only the portable version"
    Write-Host "  -InstallerOnly   Build only the Windows installer"
    Write-Host "  -NoBuild         Skip executable build (use existing)"
    Write-Host "  -Help            Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\build.ps1                    # Build everything"
    Write-Host "  .\build.ps1 -PortableOnly     # Portable version only"
    Write-Host "  .\build.ps1 -InstallerOnly    # Installer only"
    Write-Host "  .\build.ps1 -NoBuild -InstallerOnly  # Installer from existing exe"
    Write-Host ""
}

function Test-Prerequisites {
    Write-Info "Checking prerequisites..."
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python found: $pythonVersion"
        } else {
            Write-Error "Python not found or not in PATH"
            return $false
        }
    } catch {
        Write-Error "Python not found. Please install Python 3.8+ and add to PATH"
        return $false
    }
    
    # Check if main script exists
    if (-not (Test-Path "weather_widget_app.py")) {
        Write-Error "Main script weather_widget_app.py not found"
        return $false
    }
    
    # Check if build script exists
    if (-not (Test-Path "build_executable.py")) {
        Write-Error "Build script build_executable.py not found"
        return $false
    }
    
    return $true
}

function Test-InnoSetup {
    $innoPaths = @(
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles}\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles(x86)}\Inno Setup 5\ISCC.exe", 
        "${env:ProgramFiles}\Inno Setup 5\ISCC.exe"
    )
    
    foreach ($path in $innoPaths) {
        if (Test-Path $path) {
            Write-Success "Inno Setup found: $path"
            return $true
        }
    }
    
    Write-Warning "Inno Setup not found. Installer creation will be skipped."
    Write-Info "Download from: https://jrsoftware.org/isinfo.php"
    return $false
}

function Invoke-BuildProcess {
    param(
        [string]$BuildArgs = ""
    )
    
    Write-Info "Starting build process..."
    Write-ColorOutput "🔨 Building Hoodie Weather Widget..." "Yellow"
    Write-ColorOutput "=" * 50 "Yellow"
    
    try {
        $buildCommand = "python build_executable.py $BuildArgs"
        Write-Info "Running: $buildCommand"
        
        Invoke-Expression $buildCommand
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Build completed successfully!"
            return $true
        } else {
            Write-Error "Build failed with exit code $LASTEXITCODE"
            return $false
        }
    } catch {
        Write-Error "Build failed with exception: $($_.Exception.Message)"
        return $false
    }
}

function Show-Results {
    Write-ColorOutput "`n🎉 Build Results:" "Yellow"
    Write-ColorOutput "=" * 30 "Yellow"
    
    $hasResults = $false
    
    # Check for portable version
    if (Test-Path "HoodieWeatherWidget_Portable") {
        Write-Success "Portable Package: HoodieWeatherWidget_Portable\"
        $hasResults = $true
    }
    
    # Check for installer
    if (Test-Path "installer_output\HoodieWeatherSetup.exe") {
        $installerSize = (Get-Item "installer_output\HoodieWeatherSetup.exe").Length / 1MB
        Write-Success "Windows Installer: installer_output\HoodieWeatherSetup.exe ($([math]::Round($installerSize, 1)) MB)"
        $hasResults = $true
    }
    
    if (-not $hasResults) {
        Write-Warning "No output packages found. Check build logs for errors."
        return
    }
    
    Write-Host ""
    Write-ColorOutput "💡 Distribution Recommendations:" "Cyan"
    Write-Host "   🥇 Primary: Use HoodieWeatherSetup.exe (professional installer)"
    Write-Host "   🥈 Alternative: Use portable folder (no installation required)" 
    Write-Host "   📤 Both versions are ready for distribution"
    Write-Host ""
}

# Main execution
function Main {
    # Set console title and colors
    $host.ui.RawUI.WindowTitle = "Hoodie Weather Widget - Build System"
    
    # Show header
    Clear-Host
    Write-ColorOutput "🧥 Hoodie Weather Widget - Build System" "Yellow"
    Write-ColorOutput "=" * 50 "Yellow"
    Write-Host ""
    
    # Handle help
    if ($Help) {
        Show-Help
        return
    }
    
    # Check prerequisites
    if (-not (Test-Prerequisites)) {
        Write-Error "Prerequisites check failed. Cannot continue."
        return
    }
    
    # Build command line arguments
    $buildArgs = @()
    
    if ($PortableOnly) {
        $buildArgs += "--portable-only"
        Write-Info "Mode: Portable package only"
    } elseif ($InstallerOnly) {
        $buildArgs += "--installer-only" 
        Write-Info "Mode: Windows installer only"
        # Check Inno Setup for installer-only builds
        if (-not (Test-InnoSetup)) {
            Write-Error "Inno Setup required for installer creation"
            return
        }
    } else {
        Write-Info "Mode: Complete build (portable + installer)"
        if (-not (Test-InnoSetup)) {
            Write-Warning "Inno Setup not found. Only portable version will be created."
        }
    }
    
    if ($NoBuild) {
        $buildArgs += "--no-build"
        Write-Info "Skipping executable build (using existing)"
        
        # Verify existing executable
        if (-not (Test-Path "dist\HoodieWeather.exe")) {
            Write-Error "No existing executable found. Run without -NoBuild first."
            return
        }
    }
    
    # Execute build
    $buildArgsString = $buildArgs -join " "
    if (Invoke-BuildProcess -BuildArgs $buildArgsString) {
        Show-Results
        
        # Open output directories
        $openDirs = Read-Host "`nOpen output directories? (y/n)"
        if ($openDirs -eq "y" -or $openDirs -eq "yes") {
            if (Test-Path "HoodieWeatherWidget_Portable") {
                Invoke-Item "HoodieWeatherWidget_Portable"
            }
            if (Test-Path "installer_output") {
                Invoke-Item "installer_output"
            }
        }
    } else {
        Write-Error "Build process failed. Check the output above for details."
    }
    
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Run main function
Main
