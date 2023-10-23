#pylint: disable=line-too-long,invalid-name
'''
Python script made specifically for the mod "Andrudis QuestManiac" (AQM) to update it once again for SPT-AKI 3.7.1

Input: Drag and drop the whole AQM folder.

Output: Custom output folder structure based on AQM with all the properly formatted files.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

Written by Mighty_Condor
2023-02-22

Updated 2023-10-22
'''
import json
import os
import shutil

def main():

    '''Main Function'''

    print("\n\nThis script takes the Andrudis QuestManiac (AQM) folder and generates new json files that follow the new locale format.\n\n")

    directory = getDirectory("Enter the AQM folder. Drag and drop or enter the path here: ")

    input("Press any key to try converting.\n\n")

    aqmData = getDatabase(directory)

    print(aqmData["db"]["traders"]["Warden_Temporal_Id"]["base.json"]["location"], "\n\n")

    #Quest Bundles - Change locales from mail + quest and quests.json to new format
    #QuestBundlesOUT =               changeBundles(aqmData["db"]["QuestBundles"])
    #AlternativeBundlesOUT =         changeBundles(aqmData["_AlternativeBundles"])
    #LegacyBundlesOUT =              changeBundles(aqmData["_LegacyBundles"])
    #BarterOnlyQuestBundlesOUT =     changeBundles(aqmData["db"]["BarterOnly"]["QuestBundles"])

    #print(QuestBundlesOUT["Ammo Proficiency"]["Bashkir_Temporal_Id"]["locales"]["en.json"], "\n\n")

    #Main locales
    #localesOUT = changeLocales(aqmData["db"]["locales"])

    #Traders
    TradersOUT = changeTraders(aqmData["db"]["traders"])

    databaseOUT = {
        "db": {
            "traders": TradersOUT
        }
    }

    outputDatabase(databaseOUT, "D:\\Desktop\\output\\", True)

    input("Press any key to exit\n")


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

    return directory

def getDatabase(directory):

    database = {}

    dirList = [f for f in os.listdir(directory)]

    print("Files found:\n\n")
    print(dirList, "\n\n")    

    for entry in dirList:

        fullPath = directory + "\\" + entry

        if os.path.isfile(fullPath):

            if fullPath.endswith(".json"):

                temp_file = open(fullPath, encoding='utf-8')
                database[entry] = json.load(temp_file)
                temp_file.close()

            else: continue

        else: database[entry] = getDatabase(fullPath)

    return database

def changeBundles(bundlesIN):

    bundlesOUT = {}

    for bundle in bundlesIN:

        bundlesOUT[bundle] = {}

        for trader in bundlesIN[bundle]:

            bundlesOUT[bundle][trader] = {}
            bundlesOUT[bundle][trader]["locales"] = {}
            bundlesOUT[bundle][trader]["quests.json"] = bundlesIN[bundle][trader]["quests.json"]

            quests = bundlesOUT[bundle][trader]["quests.json"]
            for quest in quests:
                quests[quest]["QuestName"] = bundlesIN[bundle][trader]["locales"]["en"]["quest.json"][quest]["name"]
                quests[quest]["acceptPlayerMessage"] = quest + " acceptPlayerMessage"
                quests[quest]["changeQuestMessageText"] = quest + " changeQuestMessageText"
                quests[quest]["completePlayerMessage"] = quest + " completePlayerMessage"
                quests[quest]["side"] = "Pmc"
                quests[quest]["questStatus"] = {}
                if quests[quest]["location"] == "5714dc342459777137212e0b": quests[quest]["location"] = "any"

                AvailableForFinish = quests[quest]["conditions"]["AvailableForFinish"]
                AvailableForStart = quests[quest]["conditions"]["AvailableForStart"]
                Fail = quests[quest]["conditions"]["Fail"]
                for condition in AvailableForFinish:
                    if condition["_parent"] in ["LeaveItemAtLocation", "FindItem", "HandoverItem"]:
                        condition["_props"]["isEncoded"] = False

            for locale in bundlesIN[bundle][trader]["locales"]:

                mail = bundlesIN[bundle][trader]["locales"][locale]["mail.json"]
                quest = bundlesIN[bundle][trader]["locales"][locale]["quest.json"]

                bundlesOUT[bundle][trader]["locales"][locale + ".json"] = {}
                localeOUT = bundlesOUT[bundle][trader]["locales"][locale + ".json"]

                for questID in quest:

                    localeOUT[questID + " name"] = quest[questID]["name"]
                    localeOUT[questID + " note"] = quest[questID]["note"]
                    localeOUT[questID + " description"] = mail[questID + "_Description"]
                    localeOUT[questID + " startedMessageText"] = mail[questID + "_Started"]
                    localeOUT[questID + " failMessageText"] = mail[questID + "_Fail"]
                    localeOUT[questID + " successMessageText"] = mail[questID + "_Success"]
                    localeOUT[questID + " acceptPlayerMessage"] = ""
                    localeOUT[questID + " declinePlayerMessage"] = ""
                    localeOUT[questID + " completePlayerMessage"] = ""

                    for condition in quest[questID]["conditions"]:
                        localeOUT[condition] = quest[questID]["conditions"][condition]

    return bundlesOUT

def changeLocales(localesIN):

    localesOUT = {}

    for locale in localesIN:

        localesOUT[locale] = {}
        localesOUT[locale]["trading"] = {}

        for trader in localesIN[locale]["trading"]:

            localesOUT[locale]["trading"][trader] = {}

            for entry in localesIN[locale]["trading"][trader]:

                traderIdOnly = trader.replace(".json", "")

                localesOUT[locale]["trading"][trader][traderIdOnly + " " + entry] = localesIN[locale]["trading"][trader][entry]

    return localesOUT

def changeTraders(tradersIN):

    tradersOUT = {}

    for trader in tradersIN:

        tradersOUT[trader] = {
            "assort.json": tradersIN[trader]["assort.json"],
            "base.json": tradersIN[trader]["base.json"],
            "questassort.json": tradersIN[trader]["questassort.json"]
        }

        base = tradersOUT[trader]["base.json"]
        base["items_buy"] = {
            "category": [],
            "id_list": []
        }
        base["items_buy_prohibited"] = {
            "category": [],
            "id_list": []
        }

    return tradersOUT

def outputDatabase(database, outputPath, initial=False):

    if initial:
        if os.path.exists(outputPath): shutil.rmtree(outputPath)
        os.mkdir(outputPath)

    for entry in database:

        if entry.endswith(".json"):

            outputFile = open(outputPath + entry, "w", encoding='utf-8')
            json.dump(database[entry], outputFile, ensure_ascii=False, indent=4, sort_keys=True)
            outputFile.close()

        else:
            os.mkdir(outputPath + entry + "\\")
            outputDatabase(database[entry], outputPath + entry + "\\")


if __name__ == '__main__': main()
