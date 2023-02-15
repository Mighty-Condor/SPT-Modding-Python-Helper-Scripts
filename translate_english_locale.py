'''
Python script to generate translated locale json files from a single english locale json file

Input: Drag and drop *folder* with nothing inside except the english locale json.

Output: Script outputs translated json files in a new folder called "output" inside the folder with the english locale json.

WARNING: I highly recommend you make a copy of the things you are trying to convert BEFORE running this script on them! Don't be an idiot, just do it.

Obviously you need python installed to run these scripts (Google that if you need to install it...). You might also need some dependencies, I can't remember what comes with python so try it and see if it says you need to install any.

Seems to only work with pip install googletrans==3.1.0a0 version specifically at the moment....... Seems to be a problem.

Written by Mighty_Condor
2023-01-20
'''
import json
import os
import shutil
from googletrans import Translator


enable = {
        "chinese (simplified)": True,
        "czech":                True,
        "spanish":              True,
        "mexican spanish":      True,
        "french":               True,
        "german":               True,
        "hungarian":            True,
        "italian":              True,
        "japanese":             True,
        "korean":               True,
        "polish":               True,
        "portuguese":           True,
        "russian":              True,
        "slovak":               True,
        "turkish":              True
    }

def main():

    print("\n\nThis script takes a folder with an english locale json inside and translates it into the other language locale files.\n\n")
    print("Here are the currently enabled output languages that the script has selected:\n\n", )
    for x in enable: print("{:<25}".format(x + ":"), enable[x])
    print("\n\nPlease edit the script enable variable if you need to change this.\n\n")
    print("WARNING: I highly recommend you make a copy of the things you are trying to convert BEFORE running this script on them! Don't be an idiot, just do it.\n\n")

    input("Go do that if you haven't already, then press any key to continue.\n\n")

    directory = getDirectory("Enter the folder with the english locale .json inside it. Drag and drop or enter the path here: ")

    input("Press any key to try converting.\n\n")

    english_file = open("en.json", encoding='utf-8')
    english = json.load(english_file)
    english_file.close()

    translator = Translator()

    if enable["mexican spanish"]: enable["spanish"] = True

    languagesOUT = {}
    for language in [x for x in enable if enable[x]]: #List comprehension to get only the enabled languages

        if language == "mexican spanish": continue

        languagesOUT[language] = {}

        for localeEntry in english:
            translated = translator.translate(english[localeEntry], dest=language, src="english")
            if translated:
                languagesOUT[language][localeEntry] = translated.text
                print(localeEntry + " translated to " + language)

    if os.path.exists("output"): shutil.rmtree("output")
    os.mkdir("output")
    outputDirectory = directory + "\\output"

    f = {}
    for language in languagesOUT:
        f[language] = open(outputDirectory + "\\" + fileNames[language], "w", encoding='utf-8')
        json.dump(languagesOUT[language], f[language], ensure_ascii=False, indent=4)
        f[language].close()

    if enable["mexican spanish"]: shutil.copyfile(outputDirectory + "\\" + "es.json", outputDirectory + "\\" + "es-mx.json")


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

fileNames = {
        "chinese (simplified)": "ch.json",
        "czech":                "cz.json",
        "spanish":              "es.json",
        "mexican spanish":      "es-mx.json",
        "french":               "fr.json",
        "german":               "ge.json",
        "hungarian":            "hu.json",
        "italian":              "it.json",
        "japanese":             "jp.json",
        "korean":               "kr.json",
        "polish":               "pl.json",
        "portuguese":           "po.json",
        "russian":              "ru.json",
        "slovak":               "sk.json",
        "turkish":              "tu.json"
}


if __name__ == '__main__': main()