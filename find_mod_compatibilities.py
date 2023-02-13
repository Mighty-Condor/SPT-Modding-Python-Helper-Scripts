'''
Python script to find item IDs inside the filters of mod slots. Basically if you clone an attachment mod of some kind, say a reflex sight or light/laser, and want to add the new clone ID to all of the same compatibility filters, this script is meant to find those filters and create a json with all of the necessary data.

Input: Folder with nothing except main items.json and itemIDs files inside of it.

Output: A file named "output.json" inside a folder "output" that gets created by this script inside the folder you give as input. output.json will contain the necessary data points.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

TO DO:
    1. Find a way to separate out new items vs old items.... probably have to use old items.json as well?

Written by Mighty_Condor
2023-01-20
'''
import json
import os

itemsBlacklist = [
    "62e7c4fba689e8c9c50dfc38",
    "63171672192e68c5460cebc5",
    "6333f05d1bc0e6217a0e9d34",
    "62e7c7f3c34ea971710c32fc",
    "630e39c3bd357927e4007c15",
    "62e7c880f68e7a0676050c7c",
    "62ebbc53e3c1e1ec7c02c44f",
    "634e61b0767cb15c4601a877",
    "630e1adbbd357927e4007c09",
    "62e7c98b550c8218d602cbb4",
    "630e295c984633f1fb0e7c30",
    "62e7c8f91cd3fde4d503d690",
    "62ebba1fb658e07ef9082b5a",
    "630f2872911356c17d06abc5",
    "630f28f0cadb1fe05e06f004",
    "630f291b9f66a28b37094bb8",
    "62e7c72df68e7a0676050c77",
    "62ebd290c427473eff0baafb",
    "62ea7c793043d74a0306e19f",
    "630f27f04f3f6281050b94d7",
    "630f2982cdb9e392db0cbcc7",
    "634eba08f69c710e0108d386",
    "63088377b5cd696784087147",
    "630764fea987397c0816d219",
    "630769c4962d0247b029dc60",
    "630767c37d50ff5e8a1ea71a",
    "63076701a987397c0816d21b",
    "63075cc5962d0247b029dc2a",
    "630765777d50ff5e8a1ea718",
    "630765cb962d0247b029dc45",
    "633ec7c2a6918cb895019c6c",
    "633ec6ee025b096d320a3b15",
    "633ec8e4025b096d320a3b1e",
    "62e14904c2699c0ec93adc47",
    "62e15547db1a5c41971c1b5e",
    "637ba19df7ca6372bf2613d7",
    "633a98eab8b0506e48497c1a",
    "62e153bcdb1a5c41971c1b5b",
    "62ed1921b3608410ef5a2c04",
    "62ed189fb3608410ef5a2bfc",
    "62e281349ecd3f493f6df954",
    "62e2a754b6c0ee2f230cee0f",
    "637b9c37b7e3bc41b21ce71a",
    "637ba29bf7ca6372bf2613db",
    "62e27a7865f0b1592a49e17b",
    "62ff9920fe938a24c90c10d2",
    "62e2a7138e1ac9380579c122",
    "62e292e7b6c0ee2f230cee00",
    "62e2969582ebf260c20539c2",
    "62ff9faffe938a24c90c10df"
]

def main():

    print("\n\nThis script finds mod compatibilities in the main items.json file and extracts them into the custom format for my mods.\n\n")
    print("WARNING: I highly recommend you make a copy of the inputs you are trying to use BEFORE running this script on them! Don't be an idiot, just do it.\n\n")

    input("Go do that if you haven't already, then press any key to continue.\n\n")

    directory = getDirectory("Drag and drop or enter the path to the folder that the main items.json file is inside: ")
    items = loadItems(directory)
    itemIDs = getIDs(directory + "\\itemIDs.json")

    input("Press any key to try generating the output.\n\n")

    finalDict = {
        "mods": {}
    }

    for itemID in itemIDs: #For each itemID that we are looking for

        finalDict["mods"][itemID] = {}

        for item in items: #For every item in items.json

            #Check to see if this item in items.json has slots
            try: slots = items[item]["_props"]["Slots"]
            #If not, skip it
            except KeyError as error:
                #print("Exception occured at item: ", item, "\n\n")
                continue

            for slot in slots: #For each slot in the item

                #Check to see if each slot has filters
                try: filter = slot["_props"]["filters"][0]["Filter"]
                #If not, skip it
                except: 
                    print("Exception occured at slot: \n", slot)
                    continue

                for modID in filter: #For each compatible item in the slot's filter

                    if (modID == itemID): #If one of the compatible items matches the one we are looking for

                        compatibleItem = items[item]["_id"] #ID of the top-level item in items.json

                        if (compatibleItem in itemsBlacklist):
                            print("BLACKLISTED ITEM: ", compatibleItem, " slot ", slot["_name"])
                            continue

                        print("MATCH FOUND: ", compatibleItem, " slot ", slot["_name"])

                        #Check to see if the key already exists in the final dictionary
                        try: key = finalDict["mods"][itemID][compatibleItem]
                        #If not, create it
                        except:
                            finalDict["mods"][itemID][compatibleItem] = []

                        #Append the slot name into the array of the top-level item that is compatible 
                        finalDict["mods"][itemID][compatibleItem].append(slot["_name"])
                    

    print("\n\nAttempting to write to output now...")

    try:
        if os.path.exists("output"): shutil.rmtree("output")
        os.mkdir("output")
        outputDirectory = directory + "\\output"

        outputFile = open(outputDirectory + "\\output.json", "w", encoding='utf-8')
        json.dump(finalDict, outputFile, ensure_ascii=False, indent=4)
    except: error("There was an error trying to write the output folder/file", 1)

    input("\n\nDone.\n\nPress any key to exit")


def error(errorString, fatal) :

    print("\n\n" + errorString, "\n\n")
    if (fatal):
        input("Press any key to exit")
        exit()
    else:
        input("Press any key to continue, or exit manually by closing the window or CTRL+C now.")

def getDirectory(prompt):

    directory = input(prompt)

    try: directory = directory.replace('"', '')
    except: error("There was an error fixing the directory path", 1)

    print("\n\nDirectory: ", directory, "\n\n")

    try: os.chdir(directory)
    except: error("There was an error navigating to that directory", 1)

    print("Directory found!\n\n")

    return directory

def loadItems(directory):

    dirList = [f for f in os.listdir(directory) if os.path.isfile(f)]

    print("Files found:\n\n", dirList, "\n\n")

    items = {}
    try: items = json.load(open("items.json", encoding='utf-8'))
    except: error("There was an error loading items.json", 1)

    print("Items loaded\n\n")

    return items

def getIDs(path):

    itemIDs = {}
    try:
        tempFile = open(path, encoding='utf-8')
        itemIDs = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading itemIDs.json file", 1)

    print("IDs loaded\n\n")

    return itemIDs


if __name__ == '__main__':
    main()