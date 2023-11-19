# Minimum required Python version
$minimumVersion = 3

# Check if Python is installed
$pythonExecutable = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonExecutable) {
    Write-Host "Python not found. Installing Python..."
    
    # Download and install Python
    Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe -OutFile python_installer.exe
    Start-Process -Wait -FilePath .\python_installer.exe
    Remove-Item .\python_installer.exe
} else {
    # Get the installed Python version
    $installedVersion = & $pythonExecutable --version 2>&1
	Read-Host -Prompt "Press any key to continue..."


    $installedVersion = $installedVersion -match '(\d+)' ; $matches[1]

Read-Host -Prompt "Press any key to continue..."
    Write-Host "Installed Python version: $installedVersion"
Read-Host -Prompt "Press any key to continue..."

    Write-Host "Minimum required Python version: $minimumVersion"

Read-Host -Prompt "Press any key to continue..."

    if ($installedVersion -ge $minimumVersion) {
        Write-Host "Python is already installed. Version meets the requirements."
    } else {
        Write-Host "Python version $installedVersion found, but version $minimumVersion or later is required. Installing Python..."

        # Download and install Python
        Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe -OutFile python_installer.exe
        Start-Process -Wait -FilePath .\python_installer.exe
        Remove-Item .\python_installer.exe
    }
}

$gp = Get-Location
Write-Host "current git folder is: $gp"
Read-Host -Prompt "Press any key to continue..."


# Create a virtual environment
python -m venv myenv
# Activate the virtual environment
.\myenv\Scripts\Activate
Read-Host -Prompt "Press any key to continue..."
# Install pandas using pip
pip install pandas
pip install pytest
pip install pylint

$p = Get-Location
Write-Host "current folder is: $p"

Copy-Item -Path ".\data" -Destination ".\myenv\data" -Recurse
Copy-Item -Path ".\config" -Destination ".\myenv\config" -Recurse
Copy-Item -Path ".\test" -Destination ".\myenv\test" -Recurse

python main.py

Read-Host -Prompt "Press any key to continue..."




Read-Host -Prompt "Press any key to continue..."
# Deactivate the virtual environment
deactivate





