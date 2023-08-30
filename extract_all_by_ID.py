'''
Python script to extract and format all necessary database info for new guns/items by item IDs.

Input: Folder with all of the new server jsons inside of it. (Need to update this later to be more descriptive...)

Output: An output folder will be created by this script inside the folder you give as input. Inside the output folder will be all the properly formatted database files you need.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

TO DO:
    1. Add counter to itemIDs to ensure all things get extracted?
    2. Add function to automatically copy necessary bundle files from live Tarkov install
        - Compare dependencies in new and old tarkov to see if size differs - get replacement bundles?
    3. Add stimulator buffs to globals? Or a more general way of doing it?
    4. Make bundles.json output better
        - rename dependencies if they are included in the bundles for the mod

Written by Mighty_Condor
2023-01-26
'''
import json
import os
import shutil

enable = {
        "items":            True,
        "handbook":         True,
        "globals":          True,
        "locales":          True,
        "traders":          True,
        "oldLocales":       False,
        "bundles":          False,
        "copyBundles":      False,
        "clothing":         False,
        "modCompat":        False,
        "modConflicts":     False
    }

def main():

    requiredPaths = {
        "itemIDs":      "\\itemIDs.json",
        "clothingIDs":  "\\clothingIDs.json",
        "items":        [ "\\items.json", "\\itemIDs.json" ],
        "handbook":     [ "\\handbook.json", "\\itemIDs.json" ],
        "globals":      [ "\\globals.json", "\\itemIDs.json" ],
        "locales":      [ "\\locales\\", "\\globals.json", "\\itemIDs.json" ],
        "traders":      [ "\\traders\\", "\\itemIDs.json" ],
        "oldLocales":   [ "\\locales\\", "\\globals.json", "\\itemIDs.json" ],
        "bundles":      [ "\\Windows.json", "\\WindowsOLD.json", "\\itemIDs.json" ],
        "clothing":     [ "\\customization.json", "\\suits.json", "\\clothingIDs.json" ],
        "modCompat":    [ "\\items.json", "\\itemsOLD.json", "\\itemIDs.json" ],
        "modConflicts": [ "\\items.json", "\\itemsOLD.json", "\\itemIDs.json" ]
    }

    print("\n\nThis script extracts all of the relevant json data for adding a new weapon/item.\n\n")
    print("The input folder for this script needs to be formatted in a certain way in order for it to work properly. Here are the acceptable input paths that the script will recognize, as well as the necessary files required for each output type:\n\n")
    for inputPath in requiredPaths: print("{:<15}".format(inputPath + ":"), requiredPaths[inputPath])
    print("\n\nPlease note that some output files will require more than one input file to generate.\n\n")
    checkEnables()
    print("WARNING: I highly recommend you make a copy of the inputs you are trying to use BEFORE running this script on them! Don't be an idiot, just do it.\n\n")

    input("Go do that if you haven't already, then press any key to continue.\n\n")

    directory = getDirectory("Drag and drop or enter the path to the folder with all of json files inside it: ", requiredPaths)

    bundlesFolderName = ""
    if (enable["bundles"]): 
        bundlesFolderName = input("Enter the name of the bundles folder that you plan on using (usually the same as the name of the mod folder e.g. AUG, G19, TALK, etc.: ")
        if (enable["copyBundles"]): eftLiveFolder = getDirectory("\n\nDrag and drop or enter the path to your *LIVE EFT* EscapeFromTarkov_Data folder: ")

    if os.path.exists("output"): shutil.rmtree("output")
    os.mkdir("output")

    itemIDs = getIDs(directory + requiredPaths["itemIDs"])
    if (enable["clothing"] or enable["locales"] or enable["oldLocales"]): clothingIDs = getIDs(directory + requiredPaths["clothingIDs"])

    items, handbook, globals, locales, traders, oldLocales, bundles, customization, suits, modsCompatible, modsConflicting = ({} for i in range(11))
    localeIDs = []

    if (enable["items"]):
        items = getItems(directory + requiredPaths["items"][0], itemIDs)
    if (enable["handbook"]): 
        handbook = getHandbook(directory + requiredPaths["handbook"][0], itemIDs)
    if (enable["globals"] or enable["locales"] or enable["oldLocales"]): 
        globals, presetIDs = getGlobals(directory + requiredPaths["globals"][0], itemIDs)
    if (enable["traders"]): 
        traders = getTraders(directory, requiredPaths["traders"][0], itemIDs)
    if (enable["clothing"]):
        customization, suits, localeIDs = getClothing([directory + path for path in requiredPaths["clothing"]], clothingIDs)
    if (enable["bundles"] or enable["copyBundles"]): 
        bundles, bundlePaths = getBundles([directory + path for path in requiredPaths["bundles"]], items, customization, bundlesFolderName)
    if (enable["locales"] or enable["oldLocales"]): 
        locales = getLocales(directory, requiredPaths["locales"][0], itemIDs, presetIDs, localeIDs)
    if (enable["oldLocales"]): 
        oldLocales = generateOldLocales(locales)
    if (enable["modCompat"]):
        modsCompatible = getCompatibilities([directory + path for path in requiredPaths["modCompat"]], itemIDs)
    if (enable["modConflicts"]):
        modsConflicting = getConflicts([directory + path for path in requiredPaths["modConflicts"]], itemIDs)

    createOutput(directory, items, handbook, globals, locales, traders, oldLocales, bundles, bundlesFolderName, customization, suits, modsCompatible, modsConflicting)

    if (enable["copyBundles"]): copySuccess = copyBundles(directory, eftLiveFolder, bundlesFolderName, bundles, bundlePaths)

    input("Done.\n\nPress any key to exit")


def error(errorString, fatal) :

    print("\n\n\nERROR: " + errorString, "\n\n\n")
    if (fatal):
        input("Press any key to exit")
        exit()
    else:
        input("Press any key to continue, or exit manually by closing the window or CTRL+C now.")

def checkEnables():

    print("Currently enabled:\n\n")
    for x in enable: print("{:<15}".format(x + ":"), enable[x])
    print("\n\n")

    if enable["bundles"] and not (enable["items"] or enable["clothing"]):
        print("WARNING: bundles are enabled but items or clothing is not, which means there will be no output in bundles.json!\n")
    elif enable["locales"] and not (enable["items"] or enable["clothing"]):
        print("WARNING: locales are enabled but items or clothing is not, which means there will be no output for locales!\n")

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

def getIDs(path):

    IDs = {}
    try:
        tempFile = open(path, encoding='utf-8')
        IDs = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading " + os.path.split(path)[1], 1)

    print(os.path.split(path)[1].replace(".json", "") + " loaded\n\n")

    return IDs

def getItems(path, itemIDs):

    print("Attempting to extract item entries now...\n\n")

    try: 
        tempFile = open(path, encoding='utf-8')
        itemsIN = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading items.json", 1)

    itemsOUT = {}
    for ID in itemIDs:
        print("item ", ID, " extracted")
        itemsOUT[ID] = itemsIN[ID]

    print("\nDone.\n\n")

    return itemsOUT

def getHandbook(path, itemIDs):

    print("Attempting to get handbook entries now...", end=" ")

    try:
        tempFile = open(path, encoding='utf-8')
        handbookIN = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading handbook.json", 1)

    handbookOUT = {
        "Items": []
    }

    for ID in itemIDs:
        for entry in handbookIN["Items"]:
            if ( entry["Id"] == ID):
                handbookOUT["Items"].append(entry)

    print("Done.\n\n")

    return handbookOUT

def getGlobals(path, itemIDs):

    print("Attempting to extract global entries now...", end=" ")

    try:
        tempFile = open(path, encoding='utf-8') 
        globalsIN = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading globals.json", 1)

    globalsOUT = {
        "ItemPresets": {},
        "config": {
            "Mastering": []
        }
    }

    presetIDs = []
    templateIDsAdded = []
    for ID in itemIDs:

        for itemPreset in globalsIN["ItemPresets"]:
            for item in globalsIN["ItemPresets"][itemPreset]["_items"]:
                if ( item["_tpl"] == ID ):
                    globalsOUT["ItemPresets"][itemPreset] = globalsIN["ItemPresets"][itemPreset]
                    presetIDs.append(itemPreset)
        
        for mastery in globalsIN["config"]["Mastering"]:
            for templateID in mastery["Templates"]:
                if ( templateID == ID and templateID not in templateIDsAdded ):
                    globalsOUT["config"]["Mastering"].append(mastery)
                    templateIDsAdded.extend(mastery["Templates"])

    print("Done.\n\n")

    return globalsOUT, presetIDs

def getTraders(directory, tradersFolder, itemIDs):

    print("Attempting to extract trader entries now...", end=" ")

    traders = os.listdir(directory + tradersFolder)

    tradersIN = {}
    try:
        for trader in traders:
            assortPath = directory + tradersFolder + trader + "\\assort.json"
            if ( os.path.exists(assortPath) ):
                tempFile = open(directory + tradersFolder + trader + "\\assort.json", encoding='utf-8')
                tradersIN[trader] = json.load(tempFile)
                tempFile.close()
    except: error("There was an error loading the traders", 1)
    
    #print(tradersIN["5a7c2eca46aef81a7ca2145d"]["items"][0])

    tradersOUT = {}
    for trader in tradersIN:

        tradersOUT[trader] = {
            "items": [],
            "barter_scheme": {},
            "loyal_level_items": {}
        }

        for ID in itemIDs:

            for item in tradersIN[trader]["items"]:

                if ( item["_tpl"] == ID and item["parentId"] == "hideout" ):

                    tradersOUT[trader]["items"].append(item)

                    connectedItems = findConnectedItems(item["_id"], tradersIN[trader]["items"])

                    if connectedItems:
                        tradersOUT[trader]["items"].extend(connectedItems)
                        #print(item, "\n\n", connectedItems, "\n\n")

                    tradersOUT[trader]["barter_scheme"][item["_id"]] = tradersIN[trader]["barter_scheme"][item["_id"]]
                    tradersOUT[trader]["loyal_level_items"][item["_id"]] = tradersIN[trader]["loyal_level_items"][item["_id"]]

    print("Done.\n\n")

    return tradersOUT

def findConnectedItems(ID, traderItems):

    connectedItems = []
    tempItems = []

    for item in traderItems:
        if ( item["parentId"] == ID ):
            connectedItems.append(item)
            #print("Item " + item["_id"] + " is connected to " + item["parentId"])

    for item in connectedItems:
        tempItems.extend(findConnectedItems(item["_id"], traderItems)) #Scary spooky recursion
        #print(connectedItems)

    connectedItems.extend(tempItems)
    #print(ID + ": Adding to connectedItems: ", end='')
    #print(tempItems)

    return connectedItems

def getClothing(paths, clothingIDs):

    print("Attempting to extract clothing items now...", end=" ")

    customizationINPath = paths[0]
    suitsINPath = paths[1]

    try: #Load customization.json input file into customizationIN dictionary
        tempFile = open(customizationINPath, encoding='utf-8')
        customizationIN = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading customization.json", 1)

    try: #Load suits.json input file into suitsIN dictionary
        tempFile = open(suitsINPath, encoding='utf-8')
        suitsIN = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading suits.json", 1)

    customizationOUT = {}
    suitsOUT = []
    localeIDs = []

    #Get the entries in customization and suits
    for ID in clothingIDs: customizationOUT[ID] = customizationIN[ID]
    for suit in suitsIN:
        if suit["suiteId"] in clothingIDs:
            suitsOUT.append(suit)
            localeIDs.append(suit["suiteId"])

    print("Done.\n\n")

    return customizationOUT, suitsOUT, localeIDs

def getBundles(paths, items, customization, bundlesFolderName):

    print("Attempting to extract bundle/dependencies now...")

    newPath = paths[0]
    oldPath = paths[1]

    try: #Load new bundles manifest
        tempFile = open(newPath, encoding='utf-8')
        bundlesNEW = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading Windows.json", 1)

    try: #Load old bundles manifest
        tempFile = open(oldPath, encoding='utf-8')
        bundlesOLD = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading WindowsOLD.json", 1)

    bundlesOUT = {
        "manifest": []
    }
    bundlesAndDependencies = {}
    missingFromOld = set()
    prefabPaths = {}
    newPrefabPaths = {}
    combined = {}

    if ( enable["items"] and not enable["clothing"]): combined = items
    elif ( enable["clothing"] and not enable["items"]): combined = customization
    elif ( enable["clothing"] and enable["items"]): combined = items | customization

    for ID in combined:

        prefabPath = usePrefabPath = watchPrefab = ""
        prefabPaths[ID] = []
        newPrefabPaths[ID] = []

        #Get the prefab paths related to the thing we are trying to add
        try: prefabPath = combined[ID]["_props"]["Prefab"]["path"]
        except: print("No prefab path for " + combined[ID]["_name"] + ", continuing.")

        try: usePrefabPath = combined[ID]["_props"]["UsePrefab"]["path"]
        except: print("No UsePrefab path for " + combined[ID]["_name"] + ", continuing.")

        try: watchPrefab = combined[ID]["_props"]["WatchPrefab"]["path"]
        except: print("No WatchPrefab path for " + combined[ID]["_name"] + ", continuing.")

        prefabPaths[ID].append(prefabPath)
        prefabPaths[ID].append(usePrefabPath)
        prefabPaths[ID].append(watchPrefab)

        #Change the prefab paths to our mod's path format
        if ( prefabPaths[ID][0] != "" ): 
            newPrefabPaths[ID].append(bundlesFolderName + "/" + os.path.split(prefabPaths[ID][0])[1])
            bundlesAndDependencies[prefabPaths[ID][0]] = bundlesNEW[prefabPaths[ID][0]]["Dependencies"]
        else: 
            newPrefabPaths[ID].append("")

        if ( prefabPaths[ID][1] != "" ): 
            newPrefabPaths[ID].append(bundlesFolderName + "/" + os.path.split(prefabPaths[ID][1])[1])
            bundlesAndDependencies[prefabPaths[ID][1]] = bundlesNEW[prefabPaths[ID][1]]["Dependencies"]
        else: 
            newPrefabPaths[ID].append("")

        if ( prefabPaths[ID][2] != "" ): 
            newPrefabPaths[ID].append(bundlesFolderName + "/" + os.path.split(prefabPaths[ID][2])[1])
            bundlesAndDependencies[prefabPaths[ID][2]] = bundlesNEW[prefabPaths[ID][2]]["Dependencies"]
        else: 
            newPrefabPaths[ID].append("")

        #Add the new paths and their corresponding dependencies to bundlesOUT if they exist
        for index, path in enumerate(prefabPaths[ID]):
            if ( path != "" ):
                bundlesOUT["manifest"].append({
                    "key": newPrefabPaths[ID][index],
                    "dependencyKeys": bundlesNEW[prefabPaths[ID][index]]["Dependencies"]
                })
        '''
        try: combined[ID]["_props"]["Prefab"]["path"] = newPrefabPaths[ID][0]
        except: pass
        try: combined[ID]["_props"]["UsePrefab"]["path"] = newPrefabPaths[ID][1]
        except: pass
        try: combined[ID]["_props"]["WatchPrefab"]["path"] = newPrefabPaths[ID][2]
        except: pass
        '''
    for key in bundlesAndDependencies:
        for dependency in bundlesAndDependencies[key]:
            if dependency not in bundlesOLD: missingFromOld.add(dependency)

    for entry in missingFromOld:

        newBundlePath = bundlesFolderName + "/" + os.path.split(entry)[1]
        prefabPaths[entry] = [ entry ]

        bundlesOUT["manifest"].append({
            "key": newBundlePath,
            "dependencyKeys": bundlesNEW[entry]["Dependencies"]
        })
    
    #Go back and fix dependencies
    prefabPathsList = list(prefabPaths.values())
    for entry in bundlesOUT["manifest"]:
        for index, dependency in enumerate(entry["dependencyKeys"]):
            if dependency in prefabPathsList:
                entry["dependencyKeys"][index] = bundlesFolderName + "/" + os.path.split(dependency)[1]
    
    #print(missingFromOld)
    #print(newPrefabPaths)

    print("\n\nDone.\n\n")
    
    return bundlesOUT, prefabPaths

def getLocales(directory, localesFolder, itemIDs, presetIDs, localeIDs):

    print("Attempting to extract locale entries now...", end=" ")

    locales = os.listdir(directory + localesFolder)

    #print(locales)

    localesIN = {}
    try:
        for locale in locales:
            tempFile = open(directory + localesFolder + locale, encoding='utf-8')
            localesIN[locale] = json.load(tempFile)
            tempFile.close()
    except: error("There was an error loading the locales", 1)
    
    #print(localesIN["en.json"])

    if ( enable["items"] and not enable["clothing"]):       combined = itemIDs
    elif ( enable["clothing"] and not enable["items"]):     combined = localeIDs
    elif ( enable["clothing"] and enable["items"]):         combined = itemIDs + localeIDs

    localesOUT = {}
    for locale in localesIN:

        localesOUT[locale] = {}

        for ID in combined:

            name =          ID + " Name"
            shortName =     ID + " ShortName"
            description =   ID + " Description"

            try: localesOUT[locale][name] = localesIN[locale][name]
            except KeyError as error: print(name + " not found in locales")
            try: localesOUT[locale][shortName] = localesIN[locale][shortName]
            except KeyError as error: print(shortName + " not found in locales")
            try: localesOUT[locale][description] = localesIN[locale][description]
            except KeyError as error: print(description + " not found in locales")

        for presetID in presetIDs:
            localesOUT[locale][presetID] = localesIN[locale][presetID]

    print("Done.\n\n")

    return localesOUT

def generateOldLocales(locales):

    print("Attempting to generate old locale entries now...", end=" ")

    oldLocalesOUT = {}

    for locale in locales:

        oldLocalesOUT[locale] = {
            "templates": {},
            "preset": {}
        }

        for entry in locales[locale]:
        
            key = entry
            value = locales[locale][entry]
            
            if (key.find(" Name") > 0): 
                nameKey = key.replace(" Name", "")
                #print("nameKey: " + nameKey)
                oldLocalesOUT[locale]["templates"][nameKey] = {
                    "Name": value,
                    "ShortName": "",
                    "Description": ""
                }
                
            elif (key.find(" ShortName") > 0): 
                shortNameKey = key.replace(" ShortName", "")
                #print("shortNameKey: " + shortNameKey)
                oldLocalesOUT[locale]["templates"][shortNameKey]["ShortName"] = value
                
            elif (key.find(" Description") > 0): 
                descriptionKey = key.replace(" Description", "")
                #print("descriptionKey: " + descriptionKey)
                oldLocalesOUT[locale]["templates"][descriptionKey]["Description"] = value
                
            else: 
                presetKey = key
                #print("presetKey: " + presetKey)
                oldLocalesOUT[locale]["preset"][presetKey] = {
                    "Name": value
                }
    
    print("Done.\n\n")

    return oldLocalesOUT

def getCompatibilities(paths, itemIDs):

    print("Attempting to find item compatibilities now...\n\n")

    try: 
        tempFile = open(paths[0], encoding='utf-8')
        itemsNEW = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading items.json", 1)

    try: 
        tempFile = open(paths[1], encoding='utf-8')
        itemsOLD = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading itemsOLD.json", 1)

    #Create item blacklist from new and old items.json
    all_itemsNEW_keys = []
    all_itemsOLD_keys = []

    for key in itemsNEW: all_itemsNEW_keys.append(key)
    for key in itemsOLD: all_itemsOLD_keys.append(key)

    itemsBlacklist = []

    for key in all_itemsNEW_keys:
        if key not in all_itemsOLD_keys:
            itemsBlacklist.append(key)

    modsCompatible = {
        "mods": {}
    }

    for itemID in itemIDs: #For each itemID that we are looking for

        modsCompatible["mods"][itemID] = {}

        for item in itemsNEW: #For every item in items.json

            #Check to see if this item in items.json has slots
            try: slots = itemsNEW[item]["_props"]["Slots"]
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

                        compatibleItem = itemsNEW[item]["_id"] #ID of the top-level item in items.json

                        if (compatibleItem in itemsBlacklist):
                            print("BLACKLISTED ITEM: ", compatibleItem, " slot ", slot["_name"])
                            continue

                        print("MATCH FOUND: ", compatibleItem, " slot ", slot["_name"])

                        #Check to see if the key already exists in the final dictionary
                        try: key = modsCompatible["mods"][itemID][compatibleItem]
                        #If not, create it
                        except:
                            modsCompatible["mods"][itemID][compatibleItem] = []

                        #Append the slot name into the array of the top-level item that is compatible 
                        modsCompatible["mods"][itemID][compatibleItem].append(slot["_name"])

    print("\n\nDone.\n\n")

    return modsCompatible

def getConflicts(paths, itemIDs):

    print("Attempting to find item conflicts now...\n\n")

    try: 
        tempFile = open(paths[0], encoding='utf-8')
        itemsNEW = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading items.json", 1)

    try: 
        tempFile = open(paths[1], encoding='utf-8')
        itemsOLD = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading itemsOLD.json", 1)

    #Create item blacklist from new and old items.json
    all_itemsNEW_keys = []
    all_itemsOLD_keys = []

    for key in itemsNEW: all_itemsNEW_keys.append(key)
    for key in itemsOLD: all_itemsOLD_keys.append(key)

    itemsBlacklist = []

    for key in all_itemsNEW_keys:
        if key not in all_itemsOLD_keys:
            itemsBlacklist.append(key)

    modsConflicting = {}

    for itemID in itemIDs: #For each itemID that we are looking for

        modsConflicting[itemID] = []

        for item in itemsNEW: #For every item in items.json

            #Check to see if this item in items.json has ConflictingItems
            try: conflictingItems = itemsNEW[item]["_props"]["ConflictingItems"]
            #If not, skip it
            except KeyError as error:
                #print("Exception occured at item: ", item, "\n\n")
                continue

            for conflictingItem in conflictingItems: #For each conflicting item

                if (conflictingItem == itemID): #If one of the conflicting items matches the one we are looking for

                    topLevelItem = itemsNEW[item]["_id"] #ID of the top-level item in items.json

                    if (topLevelItem in itemsBlacklist):
                        print("BLACKLISTED ITEM: ", topLevelItem)
                        continue

                    print("MATCH FOUND: ", topLevelItem)

                    #Append the top-level item that has a conflict into the array of the new item
                    modsConflicting[itemID].append(topLevelItem)

    print("\n\nDone.\n\n")

    return modsConflicting

def createOutput(directory, items, handbook, globals, locales, traders, oldLocales, bundles, bundlesFolderName, customization, suits, modsCompatible, modsConflicting):

    print("Attempting to write to output now...\n\n")

    directories = {
        "items":        directory + "\\output\\database\\templates\\",
        "handbook":     directory + "\\output\\database\\templates\\",
        "globals":      directory + "\\output\\database\\",
        "locales":      directory + "\\output\\database\\locales\\global\\",
        "traders":      directory + "\\output\\database\\traders\\",
        "oldLocales":   directory + "\\output\\database\\old_locales\\",
        "bundles":      directory + "\\output\\",
        "copyBundles":  directory + "\\output\\bundles\\" + bundlesFolderName + "\\",
        "clothing":     [ directory + "\\output\\database\\templates\\", directory + "\\output\\database\\traders\\5ac3b934156ae10c4430e83c\\", ],
        "modCompat":    directory + "\\output\\database\\",
        "modConflicts": directory + "\\output\\database\\"
    }

    if (enable["items"]):
        if not os.path.exists(directories["items"]): os.makedirs(directories["items"])
        itemsOutputFile = open(directories["items"] + "items.json", "w", encoding='utf-8')
        json.dump(items, itemsOutputFile, ensure_ascii=False, indent=4)
        itemsOutputFile.close()

    if (enable["handbook"]):
        if not os.path.exists(directories["handbook"]): os.makedirs(directories["handbook"])
        handbookOutputFile = open(directories["handbook"] + "handbook.json", "w", encoding='utf-8')
        json.dump(handbook, handbookOutputFile, ensure_ascii=False, indent=4)
        handbookOutputFile.close()

    if (enable["globals"]):
        if not os.path.exists(directories["globals"]): os.makedirs(directories["globals"])
        globalsOutputFile = open(directories["globals"] + "globals.json", "w", encoding='utf-8')
        json.dump(globals, globalsOutputFile, ensure_ascii=False, indent=4)
        globalsOutputFile.close()

    if (enable["locales"]):
        os.makedirs(directories["locales"])
        localesOutputFiles = {}
        for locale in locales:
            localesOutputFiles[locale] = open(directories["locales"] + locale, "w", encoding='utf-8')
            json.dump(locales[locale], localesOutputFiles[locale], ensure_ascii=False, indent=4)
            localesOutputFiles[locale].close()

    if (enable["traders"]):
        os.makedirs(directories["traders"])
        tradersOutputFiles = {}
        for trader in traders:
            os.mkdir(directories["traders"] + trader)
            tradersOutputFiles[trader] = open(directories["traders"] + trader + "\\assort.json", "w", encoding='utf-8')
            json.dump(traders[trader], tradersOutputFiles[trader], ensure_ascii=False, indent=4)
            tradersOutputFiles[trader].close()

    if (enable["oldLocales"]):
        os.makedirs(directories["oldLocales"])
        oldLocalesOutputFiles = {}
        for locale in oldLocales:
            oldLocalesOutputFiles[locale] = open(directories["oldLocales"] + locale, "w", encoding='utf-8')
            json.dump(oldLocales[locale], oldLocalesOutputFiles[locale], ensure_ascii=False, indent=4)
            oldLocalesOutputFiles[locale].close()

    if (enable["bundles"]):
        bundlesOutputFile = open(directories["bundles"] + "bundles.json", "w", encoding='utf-8')
        json.dump(bundles, bundlesOutputFile, ensure_ascii=False, indent=4)
        bundlesOutputFile.close()

    if (enable["copyBundles"]):
        if not os.path.exists(directories["copyBundles"]): os.makedirs(directories["copyBundles"])
        os.mkdir(directories["copyBundles"] + "replacement_bundles\\")

    if (enable["clothing"]):
        if not os.path.exists(directories["clothing"][0]): os.makedirs(directories["clothing"][0])
        if not os.path.exists(directories["clothing"][1]): os.makedirs(directories["clothing"][1])
        customizationOutputFile = open(directories["clothing"][0] + "customization.json", "w", encoding='utf-8')
        suitsOutputFile = open(directories["clothing"][1] + "suits.json", "w", encoding='utf-8')
        json.dump(customization, customizationOutputFile, ensure_ascii=False, indent=4)
        json.dump(suits, suitsOutputFile, ensure_ascii=False, indent=4)
        customizationOutputFile.close()
        suitsOutputFile.close()
    
    if (enable["modCompat"]):
        if not os.path.exists(directories["modCompat"]): os.makedirs(directories["modCompat"])
        modsCompatibleOutputFile = open(directories["modCompat"] + "mods_compatible.json", "w", encoding='utf-8')
        json.dump(modsCompatible, modsCompatibleOutputFile, ensure_ascii=False, indent=4)
        modsCompatibleOutputFile.close()

    if (enable["modConflicts"]):
        if not os.path.exists(directories["modConflicts"]): os.makedirs(directories["modConflicts"])
        modsConflictingOutputFile = open(directories["modConflicts"] + "mods_conflicting.json", "w", encoding='utf-8')
        json.dump(modsConflicting, modsConflictingOutputFile, ensure_ascii=False, indent=4)
        modsConflictingOutputFile.close()    

def copyBundles(directory, eftLiveFolder, bundlesFolderName, bundles, bundlePaths):

    print("Attempting to copy all necessary bundle files now...")

    copySuccess = True

    destinationFolder = directory + "\\output\\bundles\\" + bundlesFolderName + "\\"
    sourceFolder = eftLiveFolder + "\\StreamingAssets\\Windows\\"

    filenames = set()
    for entry in bundlePaths:
        for bundlePath in bundlePaths[entry]:

            if bundlePath != "":

                source = sourceFolder + os.path.normpath(bundlePath)
                filepath, filename = os.path.split(source)

                if filename in filenames:
                    temp = filepath.split(os.path.sep)
                    temp2 = temp[len(temp)-1]
                    filename = temp2 + "_" + filename
                    
                else: filenames.add(filename)
                
                destination = destinationFolder + filename

                print("Attempting to copy: ", source, "\nTo: ", destination, end="...")

                try: shutil.copyfile(source, destination)
                except:
                    error("There was an error copying file: " + filename, 0)
                    copySuccess = False

                print("Success!")

    print("\n\nDone.\n\n")

    return copySuccess


if __name__ == '__main__': main()