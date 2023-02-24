# SPT Modding Python Helper Scripts
 
Python scripts used by me to help automate certain SPT modding tasks. 

**WARNING:** Please do not use these scripts if you do not know what you are doing/do not understand exactly how they operate. I am not responsible for any data loss you may encounter...

**Disclaimer:** I made these to use personally, they are not perfect in any way whatsoever. If anyone happens to ever read this, hopefully they can help you in some way. Also note that I will probably not update these by request.

**Disclaimer #2:** These were all made for SPT version 3.4.1. It is very possible and even likely that the way SPT works has changed in some way, so these scripts might not work perfectly or at all for newer versions.

Summary of each script's intended use:


### aqm_generate_new_locales.py

Specifically made for Andrudis-QuestManiac in order to update the necessary locale json files for it to work again. There is not really any general use for this I don't think.

### compare_items_files.py

Load two items.json type files and print to console a list of IDs that are in the second file but not the first. Can be used to extract all new keys in items.json if you enter the old items.json as the first file and the new items.json as the second file. Only works one way.

### compare_items_files_2.py

Compare two items.json files to see if there are differences between all of the included entries in the *second* items.json file. My use case is to check my mod's items.json with the main items.json to find if BSG has updated anything since I first obtained the item entries.

### extract_all_by_ID.py

Extract all related information to port a new gun from a new Tarkov wipe to SPT. Automatically format it to my mod framework and output it. This is the largest of the scripts and the most complex. It is also not perfect! Will not do 100% of the things you need for my mod framework, but will do a lot of it. Requires manual review after output is generated.

### extract_all_talk_values.py

Extract all the json values related to bot voicelines and put them into an output json.

### find_mod_compatibilities.py

Generates an output json file with the mod compatibilites for a list of item IDs. Example - say you want to port a new weapon to SPT and that includes new weapon mods like sights, stocks, foregrips, etc. Use this script to find what these new item IDs are compatible with by using the new items.json from the new wipe. Alternatively you can use this to find compatibilities for items that you clone by inputting the clone IDs and the current SPT items.json. It is probably better to do this all in your mod however, so keep that in mind.

### find_mod_conflicts.py

Same as find_mod_compatibilities but for the ConflictingITems array.

### generate_presets.py

Script used in my AI voiceline mod to auto-generate the presets based on the default json values. Input file defaults.json must be generated with extract_all_talk_values.py or be in the same format as the output of extract_all_talk_values.py.

### manually_add_to_all_locales.py

Script to manually add locale entries to every locale instead of copy pasting a whole bunch of times.

### new_locales_to_old_locales.py

Script to change locale format from new single-line 3.4.X and newer format to old multi-line format. (Why would you want to do this? Only reason I made it was for backwards-compatibility for the gun mods. Don't know if there is any other reason)

### old_locales_to_new_locales.py

Script to change locale format from old pre-3.4 format to new single-line format post-3.4 SPT. Changes a folder with how ever many locale json files you want.

### remove_files_from_folders.py

This script takes a folder that is filled with other folders that have files in them and moves all of the files up a level in the hierarchy and appends the folder name to each file's name. Be careful with this one if you decide to try and use it...

### search_all_jsons_for_string.py

Intended to search an SPT install's database folder and all jsons nested inside it for a string match. Change the string by editing the python file or edit the python file to input the string some other way. Please be careful with this one as it is recursive and only tested on the SPT database folder. Could cause PC problems if you use it on some other folder.

### translate_english_locale.py

Experimental script to automatically translate (based on google translator I believe) an english locale file to all the other locales. This will probably not work sadly.