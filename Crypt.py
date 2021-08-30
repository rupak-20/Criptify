import ray
import time
import datetime
import os.path
from cryptography.fernet import Fernet

ray.init()

#find difference between list1 and list2...used here for finding newly connected or disconnected drive
def difference(list1, list2):
    list_difference = [item for item in list1 if item not in list2]
    return list_difference

#def driveConnected():
#    print("New drive connected")

#def driveDisconnected():
#    print("Drive disconnected")


#load key from current directory
def load_key():
    return open("key.key", "rb").read()


#encryption
@ray.remote
def encryption(path, key):

    number_of_files = 0
    progress = 0
    f = Fernet(key)
    print("encrypting files...")

    for dirpath, dirnames, files in os.walk(path):
        for file in files:
            
            number_of_files = len(files)
            file_location = dirpath + "\\" + file
            with open(file_location, "rb") as data:

                file_data = data.read() # read all file data
                encrypted_data = f.encrypt(file_data)   # encrypt data

                # write the encrypted file
                with open(file_location, "wb") as data:
                    data.write(encrypted_data)
            
            progress += 1//number_of_files*100
            print(int(progress), '% completed', end = '\r')


    print("\nencrypted", number_of_files, "files. Encryption completed in ", end='')

    return (datetime.datetime.now(), str(number_of_files) + " encrypted", "0 skipped")


#decryption
@ray.remote
def decryption(path, key):

    number_of_files = 0
    skipped = []
    progress = 0
    f = Fernet(key)
    print("decrypting files...")


    for dirpath, dirnames, files in os.walk(path):
        for file in files:
            
            number_of_files = len(files)
            file_location = dirpath + "\\" + file
            with open(file_location, "rb") as data:
                
                encrypted_data = data.read()    # read the encrypted data
                try:
                    decrypted_data = f.decrypt(encrypted_data)  # decrypt data
                except:
                    skipped.append(file_location)
                    progress += 1//number_of_files*100
                else:
                    # write the original file
                    with open(file_location, "wb") as data:
                        data.write(decrypted_data)
            
            progress += 1//number_of_files*100
            print(int(progress), '% completed', end = '\r')

    print("\ndecrypted", number_of_files, "files")
    if(len(skipped) > 0):
        print("skipped", len(skipped), "files. Files were either invalid of modified previously")
    print("Decryption completed in ", end='')

    return (datetime.datetime.now(), str(number_of_files) + " decrypted", str(len(skipped)) + " skipped")


#driver code
if __name__ == '__main__':
    
    #list of possible drives
    driveList = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    drives = ['%s:' % d for d in driveList if os.path.exists('%s:' % d)]    #connected drives
    crypt = False
    controller = False       #to avoid encrpting an already encrypted drive
    print("connect a USB drive to start the process")
    key = load_key()

    while True:

        #finding newly connected or disconnected drives
        uncheckedDrives = ['%s:' % d for d in driveList if os.path.exists('%s:' % d)]
        x = difference(uncheckedDrives, drives)

        #if drive is connected
        if x:
            print(x[0], "drive connected")
#            driveConnected()
            start = time.time()

            for i in x:
                path = i + "\\"     #path of the drive
                
                #encrypt files
                if crypt == False and controller == False:

                    log = encryption.remote(path, key)    #encryption process
                    log = ray.get(log)
                    
                    finish = time.time()
                    print(finish - start, "seconds")
                    crypt = True


                #decrypt files
                elif crypt == True and controller == True:

                    log = decryption.remote(path, key)    #decryption process
                    log = ray.get(log)

                    finish = time.time()
                    print(finish - start, "seconds")
                    crypt = False

        x = difference(drives, uncheckedDrives)
        #if drive is disconnected
        if x:

            if controller:
                controller = False
            else:
                controller = True

            print(str(x[0]) + " drive removed")
#            driveDisconnected()

        drives = ['%s:' % d for d in driveList if os.path.exists('%s:' % d)]

        time.sleep(1)


#roadmap:

    #solve multiple encryption problem
    #add manual control
    #add support for argparser to run application on cli
    #add password protection
    #support encryption of large files
    #create a dedicated website
    #containerize the app using docker
    #create and distribute executables and docker images
    #add support for log files
    #add RSA encryption
    #(maybe) add GUI