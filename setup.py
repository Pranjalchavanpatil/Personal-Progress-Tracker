import cx_Freeze
import sys
import os 
base = None

if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\tcl\tk8.6"

executables = [cx_Freeze.Executable("personal_progress_tracker.py", base=base, icon="6.ico")]


cx_Freeze.setup(
    name = "Personal Progress Tracker",
    options = {"build_exe": {"packages":["tkinter","os","httplib2"], "include_files":["6.ico","socks.py",'tcl86t.dll','tk86t.dll', 'images','ppt',"AB_dashboard.py","achievments.py","add_sgpa.py","certificates.py","feedback.py","graph.py","marks.py","share_pdf.py","skills.py"]}},
    version = "1.0",
    description = "Personal Progress Tracker  | Developed By Satyam Gurav",
    executables = executables
    )
