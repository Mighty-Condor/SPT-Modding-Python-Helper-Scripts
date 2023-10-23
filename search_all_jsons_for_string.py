'''
Python script to search all nested jsons for a sting.

Input: Folder with all of the jsons you want to search inside it, including jsons inside other folders. The script will only find json files and not other files.

Output: No actual output except the console which will tell you in which files it found a match.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

Written by Mighty_Condor
2023-01-26
'''
import json
import os
import shutil

stringToFind = "WEAPON_SKILL_REPAIR_GAIN"

def main():

    print("\n\nThis script searches all nested jsons for a string match and prints which files have the string in the console.\n\n")
    print("WARNING: I highly recommend you make a copy of the inputs you are trying to use BEFORE running this script on them! Don't be an idiot, just do it.\n\n")

    input("Go do that if you haven't already, then press any key to continue.\n\n")

    directory = getDirectory("Drag and drop or enter the path to the folder with all of json files inside it: ")

    jsonPaths = getAllJsonFiles(directory)
    jsonFullPaths = [directory + x for x in jsonPaths]

    for path in jsonFullPaths:

        #print(path)

        try: jsonFile = open(path, encoding='utf-8')
        except: error("There was an error loading " + path, 1)

        jsonString = jsonFile.read()
        jsonFile.close()

        if ( jsonString.find(stringToFind) != -1): print("MATCH: ", path)


def error(errorString, fatal) :

    print("\n\n\nERROR: " + errorString, "\n\n\n")
    if (fatal):
        input("Press any key to exit")
        exit()
    else:
        input("Press any key to continue, or exit manually by closing the window or CTRL+C now.")

def getDirectory(prompt, requiredPaths=None):

    directory = input(prompt)

    try: 
        directory = os.path.normpath(directory)
        directory = directory.replace('"', '')
    except: error("There was an error fixing the directory path", 1)

    print("\n\nDirectory: ", directory, "\n\n")

    try: os.path.exists(directory)
    except: error("Directory does not exist at that path.", 1)
    print("Directory found!\n\n")

    if requiredPaths != None: 
        os.chdir(directory)

        dirList = os.listdir(directory)

        print("Found directory contents:\n\n")
        print(dirList, "\n\n\nChecking requirements now...\n\n")

        errorFlag = 0
        for output in requiredPaths:
            if ( output == "itemIDs" ):
                if not os.path.exists(directory + requiredPaths["itemIDs"]):
                    print("Missing input file or folder " + requiredPaths["itemIDs"] + " for output " + output)
                    errorFlag = 1     
            elif ( output == "clothingIDs" ):
                if not os.path.exists(directory + requiredPaths["clothingIDs"]):
                    print("Missing input file or folder " + requiredPaths["clothingIDs"] + " for output " + output)
                    errorFlag = 1                    
            elif ( enable[output] ):
                for path in requiredPaths[output]:
                    if not os.path.exists(directory + path):
                        print("Missing input file or folder " + path + " for output " + output)
                        errorFlag = 1
        
        if (errorFlag): error("Please fix the required input files or change the enabled outputs and run the script again", 1)
        else: print("All required files found!\n\n")

    return directory

def getAllJsonFiles(directory):

    jsonPaths = []
    tempFiles = []

    jsonPaths = ["\\" + f for f in os.listdir(directory) if (os.path.isfile(directory + "\\" + f) and f.endswith(".json"))]
    foldersList = ["\\" + f for f in os.listdir(directory) if os.path.isdir(directory + "\\" + f)]

    if foldersList:
        for folder in foldersList:
            tempFiles = getAllJsonFiles(directory + folder)
            tempFiles = ["\\" + folder + f for f in tempFiles]
            jsonPaths.extend(tempFiles)

    return jsonPaths

if __name__ == '__main__': main()