import os
import subprocess
import sys

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def upgrade_pip():
    """Upgrade pip to the latest version."""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])

def create_virtual_env(env_name):
    """Create a virtual environment."""
    subprocess.check_call([sys.executable, '-m', 'venv', env_name])

def main():
    env_name = '.venv'

    # Check if the virtual environment already exists
    if not os.path.exists(env_name):
        print(f"Creating virtual environment: {env_name}")
        create_virtual_env(env_name)
    else:
        print(f"Virtual environment '{env_name}' already exists.")

    # Activate the virtual environment
    activate_script = os.path.join(env_name, 'bin', 'activate_this.py')
    if os.path.exists(activate_script):
        with open(activate_script) as f:
            exec(f.read(), dict(__file__=activate_script))

    # Upgrade pip
    print("Upgrading pip...")
    upgrade_pip()

    # Install required packages
    print("Installing required packages...")
    try:
        install('mediapipe==0.10.21')  # You can specify a version if needed
    except subprocess.CalledProcessError:
        print("Failed to install mediapipe. Please install it manually.")
    
    try:
        install('opencv-python')
    except subprocess.CalledProcessError:
        print("Failed to install opencv-python. Please install it manually.")

    try:
        install('pyautogui')  # Add pyautogui installation
    except subprocess.CalledProcessError:
        print("Failed to install pyautogui. Please install it manually.")

    print("Setup complete! You can now run your hand tracking application.")

if __name__ == "__main__":
    main() 