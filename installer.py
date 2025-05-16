import shutil
import os
import getpass
import sys

user = getpass.getuser()
startup = fr"C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

python_v = sys.version.split()[0].replace('.', '')[:3]

pythonw_location = fr"C:\Users\{user}\AppData\Local\Programs\Python\Python{python_v}\pythonw.exe"






