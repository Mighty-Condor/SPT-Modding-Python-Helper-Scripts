import os
import shutil

print("\n\nThis script takes a folder that is filled with other folders that have files in them and moves all of the files up a level in the hierarchy and appends the folder name to each file's name.\n\n")
print("Note that if there are folders inside the folders inside the top folder it might not work properly...\n\n")

directory = input("Enter the top-level folder that you want all the files to go in to: ")

try: directory.replace('"', '')
except:
    print("There was an error fixing the directory path")
    input("Press any key to exit")
    exit()

print("\n\nDirectory: ", directory)
print("Press any key to continue")

input()

try: os.chdir(directory)
except:
    print("There was an error navigating to that directory")
    input("Press any key to exit")
    exit()

dirList = os.listdir(directory)

print(dirList)

#Create temporary backup directory:

print("\n\nCreating temporary backup directory...\n")

os.chdir("..")
tempDirectory = os.getcwd()
try: tempBackup = shutil.copytree(directory, tempDirectory + "\\" + "tempBackup")
except:
    print("There was an error creating the backup directory")
    input("Press any key to exit")
    exit()
os.chdir(directory)
    
print("Done!\n\n")

for x in dirList:

    #print(directory + "\\" + x)

    for y in os.listdir(directory + "\\" + x):
        #print(directory + "\\" + x)
        #print(y)
        #print(directory + "\\" + x + "\\" + y, directory + "\\" + "[" + x + "] " + y)
        try: os.rename(directory + "\\" + x + "\\" + y, directory + "\\" + "[" + x + "] " + y)
        except:
            print("There was an error with: " + directory + "\\" + x + "\\" + y)
            print("\n\nSelect an option to continue or exit: ")
            print("\n\n1. Continue with the program")
            print("2. Exit now as-is (WARNING: will immediately exit the program)")
            print("3. Undo everything that has been done")
            
            optionNumber = input("\n\nEnter option number: ")
            
            if int(optionNumber) == 1: pass
            
            elif int(optionNumber) == 2: exit()
            
            elif int(optionNumber) == 3:
                os.chdir("..")
                try: shutil.rmtree(directory)
                except:
                    print("Couldn't remove the working directory")
                    input("Press any key to exit")
                    exit()
                try: os.rename("tempBackup", directory)
                except:
                    print("Couldn't rename the backup directory")
                    input("Press any key to exit")
                    exit()
                os.chdir(directory)
                
            else: 
                print("Something went wrong.")
                input("Press any key to exit")
                exit()
        
    try: os.rmdir(directory + "\\" + x)
    except:
        print("There was an error removing this directory: " + directory + "\\" + x)

deleteBackup = input("Do you want to remove the backup folder now?\n\nNow might be a good time to make sure everything is in its place!\n\nY or N: ")

if deleteBackup == "Y":
    os.chdir("..")
    try: shutil.rmtree("tempBackup")
    except: 
        print("Couldn't remove the backup directory")
        input("Press any key to exit")
        exit()
    os.chdir(directory)

elif deleteBackup == "N":
    input("Press any key to exit")
    
else:
    print("Either you didn't enter Y or N; or something else went wrong.")
    input("Press any key to exit (Backup will be kept - can manually delete it :-)")
    
exit()