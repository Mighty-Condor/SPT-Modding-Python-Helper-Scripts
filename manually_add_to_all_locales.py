'''
Python script to change manually add locale entries to every locale instead of copy pasting a whole bunch of times.

Input: Drag and drop *folder* with nothing inside except the locale jsons that you want to convert and a file named localeEntries.json.

Output: Script outputs same-name json files in a new folder called "output" inside the folder with the original locale jsons.

WARNING: I highly recommend you make a copy of the things you are trying to convert BEFORE running this script on them! Don't be an idiot, just do it.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

Written by Mighty_Condor
2023-02-05s
'''
import json
import os
import shutil

def main():

    requiredPaths = {
        "locales":          "\\locales\\",
        "localeEntries":    "\\localeEntries.json"
    }

    print("\n\nThis script takes a folder that has a folder with locale .json files and a localeEntries.json file inside it and adds entries from a separate file manually.\n\n")

    print("WARNING: I highly recommend you make a copy of the things you are trying to convert BEFORE running this script on them! Don't be an idiot, just do it.\n\n")

    input("Go do that if you haven't already, then press any key to continue.\n\n")

    directory = getDirectory("Enter the folder with  the locale .jsons folder and localEntries.json inside it. Drag and drop or enter the path here: ", requiredPaths)

    input("Press any key to try converting.\n\n")

    dirList = [f for f in os.listdir(directory + requiredPaths["locales"]) if os.path.isfile(directory + requiredPaths["locales"] + f)]

    print("Files found:\n\n")
    print(dirList)

    pathList = [directory + "\\locales\\" + s for s in dirList]
    #print(pathList)

    locales = {}

    for locale in dirList:

        locale_file = open("locales\\" + locale, encoding='utf-8')
        locales[locale] = json.load(locale_file)
        locale_file.close()

    try: 
        tempFile = open("localeEntries.json", encoding='utf-8')
        localeEntries = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading localeEntries.json", 1)
        
    for locale in locales:

        for entry in localeEntries:

            locales[locale][entry] = localeEntries[entry]

    if os.path.exists("output"): shutil.rmtree("output")
    os.mkdir("output")
    outputDirectory = directory + "\\output"
    #print(outputDirectory)

    f = {}
    for locale in dirList:
        f[locale] = open(outputDirectory + "\\" + locale, "w", encoding='utf-8')
        json.dump(locales[locale], f[locale], ensure_ascii=False, indent=4)


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
            if ( output == "locales" ):
                if not os.path.exists(directory + requiredPaths["locales"]):
                    print("Missing input file or folder " + requiredPaths["itemIDs"] + " for output " + output)
                    errorFlag = 1
            elif ( output == "localeEntries" ):
                if not os.path.exists(directory + requiredPaths["localeEntries"]):
                    print("Missing input file or folder " + requiredPaths["clothingIDs"] + " for output " + output)
                    errorFlag = 1
        
        if (errorFlag): error("Please fix the required input files or change the enabled outputs and run the script again", 1)
        else: print("All required files found!\n\n")

    return directory


if __name__ == '__main__': main()