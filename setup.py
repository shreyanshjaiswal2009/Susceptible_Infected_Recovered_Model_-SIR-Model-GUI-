import sys
from cx_Freeze import setup, Executable

# Modify the following variables based on your script
script_name = "Slider_GUI_Copy.py"
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this for Windows GUI applications

# Dependencies (add any additional packages/modules your script requires)
build_exe_options = {"packages": [], "excludes": []}

# Create the executable
setup(
    name="YourAppName",
    version="1.0",
    description="Description of your application",
    options={"build_exe": build_exe_options},
    executables=[Executable(script_name, base=base)]
)
