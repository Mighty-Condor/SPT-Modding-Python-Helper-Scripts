'''
Python script to extract all of the relevant talk values for each SPT bot type at each difficulty.

Input: Folder with all of the bot type .jsons inside of it. SPT-AKI\Aki_Data\Server\database\bots\types

Output: A file named "output.json" inside a folder "output" that gets created by this script inside the folder you give as input. output.json will contain the talk values.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

Written by Mighty_Condor
2023-01-25
'''
import json
import os

def main():

    print("\n\nThis script extracts all of the relevant talk values from the bot types files in SPT.\n\n")
    print("WARNING: I highly recommend you make a copy of the inputs you are trying to use BEFORE running this script on them! Don't be an idiot, just do it.\n\n")

    input("Go do that if you haven't already, then press any key to continue.\n\n")

    directory = getDirectory("Drag and drop or enter the path to the folder with all of the bot types inside it: ")

    dirList = [f for f in os.listdir(directory) if os.path.isfile(f)]
    #print(dirList, "\n\n")

    bot_types = {}
    for bot_type in dirList:

        easy_bot_type = translate(bot_type)

        if ( easy_bot_type == None ): continue
        else: bot_types[easy_bot_type] = json.load(open(bot_type, encoding='utf-8'))

    #print(bot_types["normalScavs"]["difficulty"]["easy"]["Mind"], "\n\n")

    finalDict = {}

    for bot_type in bot_types:

        finalDict[bot_type] = {}

        for difficulty in bot_types[bot_type]["difficulty"]:

            mind = bot_types[bot_type]["difficulty"][difficulty]["Mind"]
            patrol = bot_types[bot_type]["difficulty"][difficulty]["Patrol"]
            grenade = bot_types[bot_type]["difficulty"][difficulty]["Grenade"]

            finalDict[bot_type][difficulty] = {}

            if "CAN_TALK" in mind: finalDict[bot_type][difficulty]["CAN_TALK"] = mind["CAN_TALK"]
            else: finalDict[bot_type][difficulty]["CAN_TALK"] = True

            if "TALK_WITH_QUERY" in mind: finalDict[bot_type][difficulty]["TALK_WITH_QUERY"] = mind["TALK_WITH_QUERY"]
            else: finalDict[bot_type][difficulty]["TALK_WITH_QUERY"] = True

            if "GROUP_ANY_PHRASE_DELAY" in mind: finalDict[bot_type][difficulty]["GROUP_ANY_PHRASE_DELAY"] = mind["GROUP_ANY_PHRASE_DELAY"]
            else: finalDict[bot_type][difficulty]["GROUP_ANY_PHRASE_DELAY"] = None

            if "GROUP_EXACTLY_PHRASE_DELAY" in mind: finalDict[bot_type][difficulty]["GROUP_EXACTLY_PHRASE_DELAY"] = mind["GROUP_EXACTLY_PHRASE_DELAY"]
            else: finalDict[bot_type][difficulty]["GROUP_EXACTLY_PHRASE_DELAY"] = None

            if "TALK_DELAY" in patrol: finalDict[bot_type][difficulty]["TALK_DELAY"] = patrol["TALK_DELAY"]
            else: finalDict[bot_type][difficulty]["TALK_DELAY"] = None

            if "TALK_DELAY_BIG" in patrol: finalDict[bot_type][difficulty]["TALK_DELAY_BIG"] = patrol["TALK_DELAY_BIG"]
            else: finalDict[bot_type][difficulty]["TALK_DELAY_BIG"] = None

            if "MIN_TALK_DELAY" in patrol: finalDict[bot_type][difficulty]["MIN_TALK_DELAY"] = patrol["MIN_TALK_DELAY"]
            else: finalDict[bot_type][difficulty]["MIN_TALK_DELAY"] = None            

            if "MIN_DIST_TO_CLOSE_TALK" in patrol: finalDict[bot_type][difficulty]["MIN_DIST_TO_CLOSE_TALK"] = patrol["MIN_DIST_TO_CLOSE_TALK"]
            else: finalDict[bot_type][difficulty]["MIN_DIST_TO_CLOSE_TALK"] = None

            if "MIN_DIST_TO_CLOSE_TALK_SQR" in patrol: finalDict[bot_type][difficulty]["MIN_DIST_TO_CLOSE_TALK_SQR"] = patrol["MIN_DIST_TO_CLOSE_TALK_SQR"]
            else: finalDict[bot_type][difficulty]["MIN_DIST_TO_CLOSE_TALK_SQR"] = None

            if "CHANCE_TO_NOTIFY_ENEMY_GR_100" in grenade: finalDict[bot_type][difficulty]["CHANCE_TO_NOTIFY_ENEMY_GR_100"] = grenade["CHANCE_TO_NOTIFY_ENEMY_GR_100"]
            else: finalDict[bot_type][difficulty]["CHANCE_TO_NOTIFY_ENEMY_GR_100"] = None     

            if "CHANCE_TO_PLAY_VOICE_WHEN_CLOSE" in patrol: finalDict[bot_type][difficulty]["CHANCE_TO_PLAY_VOICE_WHEN_CLOSE"] = patrol["CHANCE_TO_PLAY_VOICE_WHEN_CLOSE"]
            else: finalDict[bot_type][difficulty]["CHANCE_TO_PLAY_VOICE_WHEN_CLOSE"] = 50 


    #print(finalDict, "\n\n")

    print("\n\nAttempting to write to output now...")

    try:
        os.mkdir("output")
        outputFile = open(directory + "\\output\\output.json", "w", encoding='utf-8')
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

def translate(filename):
    
    translationDict = {
        "assault.json":                 "normalScavs",
        "marksman.json":                "sniperScavs", 
        "cursedassault.json":           "taggedAndCursedScavs",
        "bear.json":                    "bear",
        "usec.json":                    "usec",
        "bossbully.json":               "reshala",
        "followerbully.json":           "reshalaFollowers",
        "bossgluhar.json":              "gluhar",
        "followergluharassault.json":   "gluharFollowerAssault",
        "followergluharscout.json":     "gluharFollowerScout",
        "followergluharsecurity.json":  "gluharFollowerSecurity",
        "followergluharsnipe.json":     "gluharFollowerSnipe",
        "bosssanitar.json":             "sanitar",
        "followersanitar.json":         "sanitarFollowers",
        "bosskojaniy.json":             "shturman",
        "followerkojaniy.json":         "shturmanFollowers",
        "bosskilla.json":               "killa",
        "bosstagilla.json":             "tagilla",
        "bossknight.json":              "knight",
        "followerbigpipe.json":         "bigpipe",
        "followerbirdeye.json":         "birdeye",
        "gifter.json":                  "santa",
        "sectantpriest.json":           "cultistPriest",
        "sectantwarrior.json":          "cultistFollowers",
        "pmcbot.json":                  "raiders",
        "exusec.json":                  "rogues",
        "bosszryachiy.json":            "zryachiy",
        "followerzryachiy.json":        "zryachiyFollowers"
    }

    if filename in translationDict: return translationDict[filename]
    else: return None


if __name__ == '__main__': main()