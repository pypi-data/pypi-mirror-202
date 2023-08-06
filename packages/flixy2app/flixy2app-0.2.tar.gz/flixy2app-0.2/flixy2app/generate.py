import sys
import os
import shutil
from .converter import flixy2app_convert
try: pass
except: sys.exit("please install flet first. pip install flet --upgrade")


args = sys.argv

print("Before start, be sure that the file is on the same this cmd running dir.")
file_name = input("Enter the main file name:")

if os.path.isfile(file_name) == False:
    sys.exit("Error: no file with this name!")

r = flixy2app_convert(file_name, "your_app")
shutil.rmtree("build")

if r:
    print("Done!. Your app is on 'your_app' folder!.")
    print("Go share your experience with the community!! : https://github.com/SKbarbon/flixy/discussions/categories/general")