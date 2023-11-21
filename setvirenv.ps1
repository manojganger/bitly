# Minimum required Python version
$minimumVersion = 3

# Check if Python is installed
$pythonExecutable = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonExecutable) 
{
    Write-Host "Python not found. Installing Python..."
    
    # Download and install Python
    Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe -OutFile python_installer.exe
    Start-Process -Wait -FilePath .\python_installer.exe
    Remove-Item .\python_installer.exe
} 
else 
{
    # Get the installed Python version
    $installedVersion = & $pythonExecutable --version 2>&1

    $installedVersion = $installedVersion -match '(\d+)' ; $matches[1]

    Write-Host "Installed Python version: $installedVersion"

    Write-Host "Minimum required Python version: $minimumVersion"

    if ($installedVersion -ge $minimumVersion) 
    {
        Write-Host "Python is already installed. Version meets the requirements."
    }
    else 
    {
        Write-Host "Python version $installedVersion found, but version $minimumVersion or later is required. Installing Python..."

        # Download and install Python
        Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe -OutFile python_installer.exe
        Start-Process -Wait -FilePath .\python_installer.exe
        Remove-Item .\python_installer.exe
    }
}

$gp = Get-Location
Write-Host "current git folder is: $gp"

# Create a virtual environment
python -m venv myenv
# Activate the virtual environment
.\myenv\Scripts\Activate


# Install pandas, pytest, pylint using pip
pip install pandas --quiet
pip install pytest --quiet
pip install pylint --quiet

$p = Get-Location
Write-Host "current folder is: $p"

#copy the code into the virtual environment
Copy-Item -Path ".\data" -Destination ".\myenv\" -Recurse -Force
Copy-Item -Path ".\config" -Destination ".\myenv\" -Recurse -Force
Copy-Item -Path ".\test" -Destination ".\myenv\" -Recurse -Force
Copy-Item ".\*.py" -Destination ".\myenv"

cd myenv
$pytestPath = "./test/test_main.py"
#pytest ./test/test_main.py

$result = Invoke-Expression -Command "pytest $pytestPath"
if ($? -eq "True") 
{
    Write-Host "Tests passed successfully!"
} 
else 
{
    Write-Host "Tests failed. Return value: $result"
}

Read-Host -Prompt "Now main program will run. press any key to continue..."
python main.py

Read-Host -Prompt "Above is the output. press any key to exit..."

# Deactivate the virtual environment
.\Scripts\deactivate






