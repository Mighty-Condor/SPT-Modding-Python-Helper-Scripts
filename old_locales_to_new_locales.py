'''
Python script to change locale format from old pre-3.4.X format to new single-line format.

Input: Drag and drop *folder* with nothing inside except the locale jsons that you want to convert.

Output: Script outputs same-name json files in a new folder called "output" inside the folder with the original locale jsons.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

Written by Mighty_Condor
2023-01-20
'''
import json
import os


print("\n\nThis script takes a folder that is filled with locale .json files and transforms them to make them follow the new locale format.\n\n")

print("WARNING: I highly recommend you make a copy of the things you are trying to convert BEFORE running this script on them! Don't be an idiot, just do it.\n\n")

input("Go do that if you haven't already, then press any key to continue.\n\n")

directory = input("Enter the folder with all the locale .jsons inside it. Drag and drop or enter the path here: ")

try: directory = directory.replace('"', '')
except:
    print("There was an error fixing the directory path")
    input("Press any key to exit")
    exit()
    
print("\n\nDirectory: ", directory, "\n\n")

try: os.chdir(directory)
except:
    print("There was an error navigating to that directory")
    input("Press any key to exit")
    exit()

input("Directory found! Press any key to try converting.")
    
dirList = [f for f in os.listdir(directory) if os.path.isfile(f)]

print("Files found:\n\n")
print(dirList)

pathList = [directory + "\\" + s for s in dirList]

locale_data = {}

for locale in dirList:
    
    #print(locale)
    locale_file = open(locale, encoding='utf-8')
    locale_data[locale] = json.load(locale_file)