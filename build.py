import subprocess
import sys
import os

# --- Configuration ---
GAME_SCRIPT = 'dino.py'
EXECUTABLE_NAME = 'DinoGame'
ICON_FILE = None  # Example: 'path/to/your/icon.ico'

# --- Build Command ---
# This list holds all the arguments for the PyInstaller command.
command = [
    'pyinstaller',
    '--name', EXECUTABLE_NAME,
    '--onefile',
    '--windowed',
    '--add-data', f'images{os.pathsep}images', # os.pathsep handles ':' or ';' for you
    '--add-data', f'songs{os.pathsep}songs',
]

# Add an icon if specified
if ICON_FILE:
    command.extend(['--icon', ICON_FILE])

# Add the main script to the command
command.append(GAME_SCRIPT)


# --- Run the Build Process ---
print("-"*30)
print(f"Running PyInstaller for {GAME_SCRIPT}...")
print(f"Command: {' '.join(command)}")
print("-"*30)

try:
    # Execute the command
    subprocess.run(command, check=True)
    print("\n" + "-"*30)
    print("Build successful!")
    print(f"Executable created in the 'dist' folder: {EXECUTABLE_NAME}.exe")
    print("-"*30)

except FileNotFoundError:
    print("\nERROR: 'pyinstaller' command not found.")
    print("Please make sure PyInstaller is installed: 'pip install pyinstaller'")
    sys.exit(1)
    
except subprocess.CalledProcessError as e:
    print("\n" + "-"*30)
    print(f"An error occurred during the build process.")
    print(f"Error: {e}")
    print("-"*30)
    sys.exit(1)