import json
import os

def main():

    print("\n\n")

    items_path = getFile("Drag and drop or enter the path to the main items.json file: ")
    mod_path = getFile("Drag and drop or enter the path to the mod's items.json file: ")

    file_items = open(items_path, encoding='utf-8')
    file_mod = open(mod_path, encoding='utf-8')

    items = json.load(file_items)
    mod_items = json.load(file_mod)

    file_items.close()
    file_mod.close()

    all_item_keys = []
    all_mod_keys = []

    for key in items:
        all_item_keys.append(key)

    for key in mod_items:
        all_mod_keys.append(key)

    print(all_item_keys)
    print(all_mod_keys)

    difference = []

    for key in all_mod_keys:
        if key not in all_item_keys:
            difference.append(key)

    print(difference)

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


if __name__ == '__main__': main()