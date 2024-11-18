'''Importing necessary libraries'''

import os #this will allow us to run commands or functions that will interact with our OS
import hashlib 
from datetime import datetime
from send2trash import send2trash #library will allow us to send duplicated files to the trash

#we will start by making a function that calculates the hash of a file
def file_hasher(file_path):
    #this if loop checks to see if the specified path has exsisting files
    if not os.path.isfile(file_path):
        #prints this error message if no files are found
        print(f"File was not found or is not accessible: {file_path}")
        return None
    

    hash_md5 = hashlib.md5() #hash object
    try:
        with open(file_path, "rb") as f: #opens file and reads it in binary
            for chunk in iter(lambda: f.read(4096), b""): #will read the file in chunks of 4096 bytes to accommodate for larger files
                hash_md5.update(chunk) #updates previous object with new chucnk of data

    except Exception as e: 
        #will throw an exception if there is an error reading a specified file
        print(f"Error reading this file {file_path}: {e}")
        return None
    

    return hash_md5.hexdigest() #returns out hash object as a hex representation

#function to find duplicate files
def find_dupes(directory):

    file_hashes = {} #dictionary to store file hashes
    dupes = [] #list to store the paths of duplicate files

    for root, _, files in os.walk(directory): #getting the file path
        for file in files: #looping through all th files in the directory
            file_path = os.path.join(root, file)
            hashed_file = file_hasher(file_path) #gets the MD5 hash of files in path

            if hashed_file is None: #if the file cant be hashed, continue
                continue
            if hashed_file in file_hashes: #if the hashed file is already in our hash dictionary
                dupes.append(file_path) #move it into our duplication list
            else:
                file_hashes[hashed_file] = file_path
    
    return dupes #returns the dupicate files

    #will move duplicate files into the trash-can and log it in a .txt file
def delete_dupes(dupes, log_file):

    if not dupes: #if no duplicate files were found, print this error message:
        print("No duplicate files were found ")
        return #exit function
    
    with open(log_file, "a") as log: #open log file in append mode so it doesnt overwite exsiting logs
        for file_path in dupes: #loop through each duplicate file
            try:
                print(f"Moving all duplicate files in the specified file location ot the trash: {file_path}")
                send2trash(file_path) #sends the duplicate file to trash

                log.write(f"{datetime.now()}: Moved to trash {file_path}\n ") #write the log of what file and when it was moved to the trash

            except Exception as e:
                print(f"error moving {file_path} to the trash: {e}") #print an error if there is trouble moving the specified file to the trash

        print("Process is complete. ") #lets the user know when the program has finished iterating