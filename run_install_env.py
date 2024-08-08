import subprocess
import sys
# Path to your requirements.txt file
requirements_file = 'requirements.txt'

# Read the requirements file
with open(requirements_file) as f:
    packages = f.readlines()

# Attempt to install each package
for package in packages:
    package = package.strip()  # Remove any trailing whitespace/newline
    if package:  # Ensure the package string is not empty
        print(f"Installing {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")