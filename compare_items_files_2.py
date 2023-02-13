'''
Python script to compare two items.json files to see if there are differences between all of the included entries in the "mod" items.json file. My use case is to check my mod's items.json with the main items.json to find if BSG has updated anything since I first obtained the item entries.

Input: Two items.json files.

Output: Prints the entries by item ID that are different/have changed.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

Written by Mighty_Condor
2023-01-25
'''
import json
import os

#copyPrefabPaths is a flag to tell the script to instead copy prefab paths from an existing mod items.json to the main items.json, used in conjunction with extract_items_by_ID. If anyone else is ever using this, you probably won't want to set this to True ever...
copyPrefabPaths = False

def main():

    print("\n\n")

    items_path = getFile("Drag and drop or enter the path to the main items.json file: ")
    mod_path = getFile("Drag and drop or enter the path to the mod's items.json file: ")
    if copyPrefabPaths:
        outputDirectory = getOutputDirectory()

    file_items = open(items_path, encoding='utf-8')
    file_mod = open(mod_path, encoding='utf-8')

    items = json.load(file_items)
    mod_items = json.load(file_mod)

    difference = []

    if copyPrefabPaths:

        for mod_item in mod_items:
            items[mod_item]["_props"]["Prefab"]["path"] = mod_items[mod_item]["_props"]["Prefab"]["path"]

        try:
            outputFile = open(outputDirectory + "\\output.json", "w", encoding='utf-8')
            json.dump(items, outputFile, ensure_ascii=False, indent=4)
        except: error("There was an error trying to write the output folder/file", 1)

    else:

        for item in mod_items:
            if ( mod_items[item] == items[item] ):
                continue
            else:
                difference.append(item)

        print(difference, "\n\n")

    input("Press any key to exit")


def error(errorString, fatal) :

    print("\n\n" + errorString, "\n\n")
    if (fatal):
        input("Press any key to exit")
        exit()
    else:
        input("Press any key to continue, or exit manually by closing the window or CTRL+C now.")

def getFile(prompt):

    directory = input(prompt)

    try: directory = directory.replace('"', '')
    except: error("There was an error fixing the directory path", 1)

    print("\n\nDirectory: ", directory, "\n\n")

    try: os.path.isfile(directory)
    except: error("There was an error finding that file", 1)

    print("File found!\n\n")

    return directory

def getOutputDirectory():

    outputDirectory = input("Drag and drop or enter the path to the folder where you want the output .json: ")

    try: outputDirectory = outputDirectory.replace('"', '')
    except: error("There was an error fixing the directory path", 1)

    print("\n\nDirectory: ", outputDirectory, "\n\n")

    try: os.chdir(outputDirectory)
    except: error("There was an error navigating to that directory", 1)

    print("Directory found!\n\n")

    return outputDirectory


if __name__ == '__main__': main()