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

def main():

    print("\n\nThis script takes a folder that is filled with locale .json files and transforms them to make them follow the new locale format.\n\n")
    print("WARNING: I highly recommend you make a copy of the things you are trying to convert BEFORE running this script on them! Don't be an idiot, just do it.\n\n")

    input("Go do that if you haven't already, then press any key to continue.\n\n")

    directory = getDirectory("Enter the folder with all the locale .jsons inside it. Drag and drop or enter the path here: ")

    input("Press any key to try converting.\n\n")
        
    dirList = [f for f in os.listdir(directory) if (os.path.isfile(f) and f.endswith(".json"))]

    print("Files found:\n\n")
    print(dirList, "\n\n")

    locale_data = {}

    for locale in dirList:

        locale_file = open(locale, encoding='utf-8')
        locale_data[locale] = json.load(locale_file)
        locale_file.close()

    finalDict = {}
    for locale in locale_data:

        finalDict[locale] = {}

        for template in locale_data[locale]["templates"]:

            finalDict[locale][template + " Name"] =         locale_data[locale]["templates"][template]["Name"]
            finalDict[locale][template + " ShortName"] =    locale_data[locale]["templates"][template]["ShortName"]
            finalDict[locale][template + " Description"] =  locale_data[locale]["templates"][template]["Description"]
        
        for preset in locale_data[locale]["preset"]:

            finalDict[locale][preset] = locale_data[locale]["preset"][preset]["Name"]
        
    #print(finalDict["en.json"])

    os.mkdir("output")
    outputDirectory = directory + "\\output"

    f = {}
    for locale in dirList:
        f[locale] = open(outputDirectory + "\\" + locale, "w", encoding='utf-8')
        json.dump(finalDict[locale], f[locale], ensure_ascii=False, indent=4)
        f[locale].close()


def error(errorString, fatal) :

    print("\n\n\nERROR: " + errorString, "\n\n\n")
    if (fatal):
        input("Press any key to exit")
        exit()
    else:
        input("Press any key to continue, or exit manually by closing the window or CTRL+C now.")

def getDirectory(prompt):

    directory = input(prompt)

    try: 
        directory = os.path.normpath(directory)
        directory = directory.replace('"', '')
    except: error("There was an error fixing the directory path", 1)

    print("\n\nDirectory: ", directory, "\n\n")

    try: os.path.exists(directory)
    except: error("Directory does not exist at that path.", 1)
    print("Directory found!\n\n")

    os.chdir(directory)

    dirList = os.listdir(directory)

    print("Found directory contents:\n\n")
    print(dirList, "\n\n")

    return directory


if __name__ == '__main__': main()