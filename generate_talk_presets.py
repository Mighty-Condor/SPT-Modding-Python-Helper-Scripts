import os
import json

def main():
    
    defaultsFile = getFile("Drag and drop or enter the path to the defaults.json file: ")
    outputFolder = getDirectory("Drag and drop or enter the path to the folder where you want the output .json file to be created: ")

    try: #Load defaults file
        tempFile = open(defaultsFile, encoding='utf-8')
        defaults = json.load(tempFile)
        tempFile.close()
    except: error("There was an error loading defaults.json", 1)

    presetsOUT = {
        "normalScavs": {},
        "bear": {},
        "reshala": {},
        "gluhar": {},
        "killa": {},
        "knight": {},
        "shturman": {},
        "sanitar": {},
        "tagilla": {},
        "taggedAndCursedScavs": {},
        "rogues": {},
        "bigpipe": {},
        "birdeye": {},
        "reshalaFollowers": {},
        "gluharFollowerAssault": {},
        "gluharFollowerScout": {},
        "gluharFollowerSecurity": {},
        "gluharFollowerSnipe": {},
        "shturmanFollowers": {},
        "sanitarFollowers": {},
        "santa": {},
        "sniperScavs": {},
        "raiders": {},
        "cultistPriest": {},
        "cultistFollowers": {},
        "usec": {},
        "zryachiy": {},
        "zryachiyFollowers": {}
    }

    for botType in defaults:

        presetsOUT[botType]["off"] = {
            "CAN_TALK":                             False,
            "TALK_WITH_QUERY":                      False,
            "GROUP_ANY_PHRASE_DELAY":               999999,
            "GROUP_EXACTLY_PHRASE_DELAY":           999999,
            "TALK_DELAY":                           999999.1,
            "TALK_DELAY_BIG":                       999999.1,
            "MIN_TALK_DELAY":                       999999,
            "MIN_DIST_TO_CLOSE_TALK":               5,
            "MIN_DIST_TO_CLOSE_TALK_SQR":           25,
            "CHANCE_TO_NOTIFY_ENEMY_GR_100":        0
        }

        presetsOUT[botType]["low"] = {
            "CAN_TALK":                             True,
            "TALK_WITH_QUERY":                      False,
            "GROUP_ANY_PHRASE_DELAY":               min(defaults[botType]["normal"]["GROUP_ANY_PHRASE_DELAY"] + 10, 100),
            "GROUP_EXACTLY_PHRASE_DELAY":           min(defaults[botType]["normal"]["GROUP_EXACTLY_PHRASE_DELAY"] + 10, 100),
            "TALK_DELAY":                           min(defaults[botType]["normal"]["TALK_DELAY"] + 10, 100),
            "TALK_DELAY_BIG":                       min(defaults[botType]["normal"]["TALK_DELAY_BIG"] + 10, 100),
            "MIN_TALK_DELAY":                       min(defaults[botType]["normal"]["MIN_TALK_DELAY"] + 10, 100),
            "MIN_DIST_TO_CLOSE_TALK":               max(defaults[botType]["normal"]["MIN_DIST_TO_CLOSE_TALK"] - 2, 1),
            "MIN_DIST_TO_CLOSE_TALK_SQR":           max((defaults[botType]["normal"]["MIN_DIST_TO_CLOSE_TALK"] - 2)**2, 1),
            "CHANCE_TO_NOTIFY_ENEMY_GR_100":        max(defaults[botType]["normal"]["CHANCE_TO_NOTIFY_ENEMY_GR_100"] - 50, 0)
        }

        presetsOUT[botType]["normal"] = {
            "CAN_TALK":                             True,
            "TALK_WITH_QUERY":                      False,
            "GROUP_ANY_PHRASE_DELAY":               defaults[botType]["normal"]["GROUP_ANY_PHRASE_DELAY"],
            "GROUP_EXACTLY_PHRASE_DELAY":           defaults[botType]["normal"]["GROUP_EXACTLY_PHRASE_DELAY"],
            "TALK_DELAY":                           defaults[botType]["normal"]["TALK_DELAY"],
            "TALK_DELAY_BIG":                       defaults[botType]["normal"]["TALK_DELAY_BIG"],
            "MIN_TALK_DELAY":                       defaults[botType]["normal"]["MIN_TALK_DELAY"],
            "MIN_DIST_TO_CLOSE_TALK":               defaults[botType]["normal"]["MIN_DIST_TO_CLOSE_TALK"],
            "MIN_DIST_TO_CLOSE_TALK_SQR":           defaults[botType]["normal"]["MIN_DIST_TO_CLOSE_TALK_SQR"],
            "CHANCE_TO_NOTIFY_ENEMY_GR_100":        defaults[botType]["normal"]["CHANCE_TO_NOTIFY_ENEMY_GR_100"]
        }

        presetsOUT[botType]["high"] = {
            "CAN_TALK":                             True,
            "TALK_WITH_QUERY":                      True,
            "GROUP_ANY_PHRASE_DELAY":               max(defaults[botType]["normal"]["GROUP_ANY_PHRASE_DELAY"] - 10, 1),
            "GROUP_EXACTLY_PHRASE_DELAY":           max(defaults[botType]["normal"]["GROUP_EXACTLY_PHRASE_DELAY"] - 10, 1),
            "TALK_DELAY":                           max(defaults[botType]["normal"]["TALK_DELAY"] - 10, 1),
            "TALK_DELAY_BIG":                       max(defaults[botType]["normal"]["TALK_DELAY_BIG"] - 10, 1),
            "MIN_TALK_DELAY":                       max(defaults[botType]["normal"]["MIN_TALK_DELAY"] - 10, 1),
            "MIN_DIST_TO_CLOSE_TALK":               min(defaults[botType]["normal"]["MIN_DIST_TO_CLOSE_TALK"] + 2, 10),
            "MIN_DIST_TO_CLOSE_TALK_SQR":           min((defaults[botType]["normal"]["MIN_DIST_TO_CLOSE_TALK"] + 2)**2, 100),
            "CHANCE_TO_NOTIFY_ENEMY_GR_100":        min(defaults[botType]["normal"]["CHANCE_TO_NOTIFY_ENEMY_GR_100"] + 50, 100)
        }

        presetsOUT[botType]["custom"] = {
            "CAN_TALK":                             True,
            "TALK_WITH_QUERY":                      False,
            "GROUP_ANY_PHRASE_DELAY":               defaults[botType]["normal"]["GROUP_ANY_PHRASE_DELAY"],
            "GROUP_EXACTLY_PHRASE_DELAY":           defaults[botType]["normal"]["GROUP_EXACTLY_PHRASE_DELAY"],
            "TALK_DELAY":                           defaults[botType]["normal"]["TALK_DELAY"],
            "TALK_DELAY_BIG":                       defaults[botType]["normal"]["TALK_DELAY_BIG"],
            "MIN_TALK_DELAY":                       defaults[botType]["normal"]["MIN_TALK_DELAY"],
            "MIN_DIST_TO_CLOSE_TALK":               defaults[botType]["normal"]["MIN_DIST_TO_CLOSE_TALK"],
            "MIN_DIST_TO_CLOSE_TALK_SQR":           defaults[botType]["normal"]["MIN_DIST_TO_CLOSE_TALK_SQR"],
            "CHANCE_TO_NOTIFY_ENEMY_GR_100":        defaults[botType]["normal"]["CHANCE_TO_NOTIFY_ENEMY_GR_100"]        
        }

    print("Attempting to write to output now...\n\n")

    os.mkdir("output")
    presetsOutputFile = open(outputFolder + "\\output\\presets.json", "w", encoding='utf-8')
    json.dump(presetsOUT, presetsOutputFile, ensure_ascii=False, indent=4)
    presetsOutputFile.close()

    input("Done.\n\nPress any key to exit")


def error(errorString, fatal) :

    print("\n\n\nERROR: " + errorString, "\n\n\n")
    if (fatal):
        input("Press any key to exit")
        exit()
    else:
        input("Press any key to continue, or exit manually by closing the window or CTRL+C now.")

def getFile(prompt):

    path = input(prompt)

    try: path = path.replace('"', '')
    except: error("There was an error fixing the file path", 1)

    print("\n\nFilepath: ", path, "\n\n")

    try: os.path.isfile(path)
    except: error("There was an error finding that file", 1)

    print("File found!\n\n")

    return path

def getDirectory(prompt):

    directory = input(prompt)

    try: directory = os.path.normpath(directory)
    except: error("There was an error fixing the directory path", 1)

    print("\n\nDirectory: ", directory, "\n\n")

    try: os.chdir(directory)
    except: error("There was an error navigating to that directory", 1)

    print("Directory found!\n\n")

    return directory

template = {
    "off": {
        "CAN_TALK": False,
        "TALK_WITH_QUERY": True,
        "GROUP_ANY_PHRASE_DELAY": 999999,
        "GROUP_EXACTLY_PHRASE_DELAY": 999999,
        "TALK_DELAY": 999999.1,
        "TALK_DELAY_BIG": 999999.1,
        "MIN_TALK_DELAY": 999999,
        "MIN_DIST_TO_CLOSE_TALK": 5,
        "MIN_DIST_TO_CLOSE_TALK_SQR": 25,
        "CHANCE_TO_NOTIFY_ENEMY_GR_100": 0
    },
    "low": {
        "CAN_TALK": None,
        "TALK_WITH_QUERY": None,
        "GROUP_ANY_PHRASE_DELAY": None,
        "GROUP_EXACTLY_PHRASE_DELAY": None,
        "TALK_DELAY": None,
        "TALK_DELAY_BIG": None,
        "MIN_TALK_DELAY": None,
        "MIN_DIST_TO_CLOSE_TALK": None,
        "MIN_DIST_TO_CLOSE_TALK_SQR": None,
        "CHANCE_TO_NOTIFY_ENEMY_GR_100": None
    },
    "normal": {
        "CAN_TALK": None,
        "TALK_WITH_QUERY": None,
        "GROUP_ANY_PHRASE_DELAY": None,
        "GROUP_EXACTLY_PHRASE_DELAY": None,
        "TALK_DELAY": None,
        "TALK_DELAY_BIG": None,
        "MIN_TALK_DELAY": None,
        "MIN_DIST_TO_CLOSE_TALK": None,
        "MIN_DIST_TO_CLOSE_TALK_SQR": None,
        "CHANCE_TO_NOTIFY_ENEMY_GR_100": None        
    },
    "high": {
        "CAN_TALK": None,
        "TALK_WITH_QUERY": None,
        "GROUP_ANY_PHRASE_DELAY": None,
        "GROUP_EXACTLY_PHRASE_DELAY": None,
        "TALK_DELAY": None,
        "TALK_DELAY_BIG": None,
        "MIN_TALK_DELAY": None,
        "MIN_DIST_TO_CLOSE_TALK": None,
        "MIN_DIST_TO_CLOSE_TALK_SQR": None,
        "CHANCE_TO_NOTIFY_ENEMY_GR_100": None
    }
}


if __name__ == '__main__': main()