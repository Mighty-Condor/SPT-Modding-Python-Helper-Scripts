'''
Python script made specifically for the mod "Andrudis QuestManiac" (AQM) to change a bunch of old locale files to the new locale format.

Input: Drag and drop the "db" folder from AQM.

Output: Custom output folder structure based on AQM with all the properly formatted files.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

Written by Mighty_Condor
2023-02-22
'''
import json
import os
import shutil

def main():

    print("\n\nThis script takes the Andrudis QuestManiac (AQM) \"db\" folder and generates new json files that follow the new locale format.\n\n")

    directory = getDirectory("Enter the \"db\" folder from AQM. Drag and drop or enter the path here: ")

    input("Press any key to try converting.\n\n")

    db = getDatabase(directory)

    print(db["locales"]["en"]["trading"]["Bashkir_Temporal_Id.json"], "\n\n")

    #Quest Bundles - Change locales from mail + quest to new format
    QuestBundlesOUT = {}

    for bundle in db["QuestBundles"]:

        QuestBundlesOUT[bundle] = {}

        for trader in db["QuestBundles"][bundle]:

            QuestBundlesOUT[bundle][trader] = {}
            QuestBundlesOUT[bundle][trader]["locales"] = {}
            QuestBundlesOUT[bundle][trader]["quests.json"] = db["QuestBundles"][bundle][trader]["quests.json"]

            quests = QuestBundlesOUT[bundle][trader]["quests.json"]
            for quest in quests:
                quests[quest]["QuestName"] = db["QuestBundles"][bundle][trader]["locales"]["en"]["quest.json"][quest]["name"]
                quests[quest]["acceptPlayerMessage"] = quest + " acceptPlayerMessage"
                quests[quest]["changeQuestMessageText"] = quest + " changeQuestMessageText"
                quests[quest]["completePlayerMessage"] = quest + " completePlayerMessage"
                quests[quest]["side"] = "Pmc"
                if quests[quest]["location"] == "5714dc342459777137212e0b": quests[quest]["location"] = "any"

            for locale in db["QuestBundles"][bundle][trader]["locales"]:

                mail = db["QuestBundles"][bundle][trader]["locales"][locale]["mail.json"]
                quest = db["QuestBundles"][bundle][trader]["locales"][locale]["quest.json"]

                QuestBundlesOUT[bundle][trader]["locales"][locale + ".json"] = {}
                localeOUT = QuestBundlesOUT[bundle][trader]["locales"][locale + ".json"]

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

    #print(QuestBundlesOUT["Ammo Proficiency"]["Bashkir_Temporal_Id"]["locales"]["en.json"], "\n\n")

    localesOUT = {}

    for locale in db["locales"]:

        localesOUT[locale] = {}
        localesOUT[locale]["trading"] = {}

        for trader in db["locales"][locale]["trading"]:

            localesOUT[locale]["trading"][trader] = {}

            for entry in db["locales"][locale]["trading"][trader]:

                traderIdOnly = trader.replace(".json", "")

                localesOUT[locale]["trading"][trader][traderIdOnly + " " + entry] = db["locales"][locale]["trading"][trader][entry]

    databaseOUT = {
        "locales": localesOUT,
        "QuestBundles": QuestBundlesOUT
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

    #print("Files found:\n\n")
    #print(dirList, "\n\n")    

    for entry in dirList:

        fullPath = directory + "\\" + entry

        if os.path.isfile(fullPath):

            temp_file = open(fullPath, encoding='utf-8')
            database[entry] = json.load(temp_file)
            temp_file.close()

        else: database[entry] = getDatabase(fullPath)
    
    return database

def outputDatabase(database, outputPath, initial=False):

    if initial:
        if os.path.exists(outputPath): shutil.rmtree(outputPath)
        os.mkdir(outputPath)

    for entry in database:

        if entry.endswith(".json"):

            outputFile = open(outputPath + entry, "w", encoding='utf-8')
            json.dump(database[entry], outputFile, ensure_ascii=False, indent=4)
            outputFile.close()

        else:
            os.mkdir(outputPath + entry + "\\")
            outputDatabase(database[entry], outputPath + entry + "\\")

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