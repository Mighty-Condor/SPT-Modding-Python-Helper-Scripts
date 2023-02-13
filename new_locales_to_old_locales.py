'''
Python script to change locale format from new single-line 3.4.X format to old multi-line format. (Why would you want to do this? Only reason I made it was for backwards-compatibility for the gun mods. Don't know if there is any other reason)

Input: Drag and drop *folder* with nothing inside except the locale jsons that you want to convert.

Output: Script outputs same-name json files in a new folder called "output" inside the folder with the original locale jsons.

WARNING: I highly recommend you make a copy of the things you are trying to convert BEFORE running this script on them! Don't be an idiot, just do it.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

Written by Mighty_Condor
2023-01-20
'''
import json
import os

print("\n\nThis script takes a folder that is filled with locale .json files and transforms them to make them follow the old locale format.\n\n")

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
#print(pathList)

locale_data = {}

for locale in dirList:
    
    #print(locale)
    locale_file = open(locale, encoding='utf-8')
    locale_data[locale] = json.load(locale_file)

finalDict = {}
    
for locale in locale_data:

    finalDict[locale] = {
        "templates": {},
        "preset": {}
    }
    #print(locale)

    for entry in locale_data[locale]:
    
        key = entry
        value = locale_data[locale][entry]
        
        if (key.find(" Name") > 0): 
            nameKey = key.replace(" Name", "")
            #print("nameKey: " + nameKey)
            finalDict[locale]["templates"][nameKey] = {
                "Name": value,
                "ShortName": "",
                "Description": ""
            }
            
        elif (key.find(" ShortName") > 0): 
            shortNameKey = key.replace(" ShortName", "")
            #print("shortNameKey: " + shortNameKey)
            finalDict[locale]["templates"][shortNameKey]["ShortName"] = value
            
        elif (key.find(" Description") > 0): 
            descriptionKey = key.replace(" Description", "")
            #print("descriptionKey: " + descriptionKey)
            finalDict[locale]["templates"][descriptionKey]["Description"] = value
            
        else: 
            presetKey = key
            #print("presetKey: " + presetKey)
            finalDict[locale]["preset"][presetKey] = {
                "Name": value
            }
    
    #print(finalDict[locale])
        
    #print(locale_data[locale]["62e7c4fba689e8c9c50dfc38 Name"])
    
#print(finalDict["en.json"])

os.mkdir("output")
outputDirectory = directory + "\\output"
#print(outputDirectory)

f = {}
for locale in dirList:
    f[locale] = open(outputDirectory + "\\" + locale, "w", encoding='utf-8')
    json.dump(finalDict[locale], f[locale], ensure_ascii=False, indent=4)
