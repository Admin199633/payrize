import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required libraries
required_libraries = [
    "openpyxl",
    "pandas",
    "requests",
    "datetime",
    "google-auth",
    "google-auth-oauthlib",
    "google-auth-httplib2",
    "google-api-python-client",
    "tkinter",
    "base64",
    "json",
    "os",
    # Add more libraries as needed
]

# Check and install required libraries if not already installed
for lib in required_libraries:
    try:
        __import__(lib)
    except ImportError:
        print(f"Installing {lib}...")
        install(lib)
        print(f"{lib} has been installed.")
