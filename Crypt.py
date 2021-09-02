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


#calling encryption
def call_encryption(path):

    number_of_files = 1
    progress = 1
    result_id = []
    skipped = []
    key = load_key()
    print("encrypting files...")

    for dirpath, dirnames, files in os.walk(path):
        for file in files:
            number_of_files += 1
            result_id.append(encryption.remote(dirpath + "\\" + file, key)) #encryption
    
    while(result_id):
        done_id, result_id = ray.wait(result_id)    #recieve object ID for completed project
        done_id= ray.get(done_id)
        progress += done_id[0][0]/number_of_files*100  #track progress
        print(int(progress), '% completed', end = '\r')
        if done_id[0][1] != '':
            skipped.append(done_id[0][1])
    
    print("\nencrypted", number_of_files - len(skipped), "files")
    if(len(skipped) > 0):
        print("skipped", len(skipped), "files. File access denied")
    print("Encryption completed in ", end = '')
    
    return (datetime.datetime.now(), number_of_files, "encrypted", len(skipped), "skipped")


#calling decryption
def call_decryption(path):

    number_of_files = 1
    skipped = []
    result_id = []
    progress = 1
    key = load_key()
    print("decrypting files...")

    for dirpath, dirnames, files in os.walk(path):
        for file in files:            
            number_of_files += 1
            result_id.append(decryption.remote(dirpath + "\\" + file, key))   #decryption

    while(result_id):
        done_id, result_id = ray.wait(result_id)    #recieve object ID for completed project
        done_id = ray.get(done_id)
        progress += done_id[0][0]/number_of_files*100  #track progress
        print(int(progress), '% completed', end = '\r')
        if done_id[0][1] != '':
            skipped.append(done_id[0][1])

    print("\ndecrypted", number_of_files - len(skipped), "files")
    if(len(skipped) > 0):
        print("skipped", len(skipped), "files. Files were either invalid of modified previously")
    print("Decryption completed in ", end='')

    return (datetime.datetime.now(), number_of_files, "decrypted", len(skipped), "skipped")


#encryption
@ray.remote
def encryption(file_location, key):
    
    f = Fernet(key)
    with open(file_location, "rb") as data:
        file_data = data.read()     # read all file data
        try:
            encrypted_data = f.encrypt(file_data)   # encrypt data
        except:
            return (1, file_location)
        else:
            # write the encrypted file
            with open(file_location, "wb") as data:
                data.write(encrypted_data)
    return (1, '')


#decryption
@ray.remote
def decryption(file_location, key):

    f = Fernet(key)
    with open(file_location, "rb") as data:
        encrypted_data = data.read()    # read the encrypted data
        try:
            decrypted_data = f.decrypt(encrypted_data)  # decrypt data
        except:
            return (1, file_location)
        else:
            # write the original file
            with open(file_location, "wb") as data:
                data.write(decrypted_data)
    return (1, '')


#driver code
if __name__ == '__main__':
    
    #list of possible drives
    driveList = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    drives = ['%s:' % d for d in driveList if os.path.exists('%s:' % d)]    #connected drives
    crypt = False
    controller = False       #to avoid encrpting an already encrypted drive
    print("connect a USB drive to start the process")

    while True:

        #finding newly connected or disconnected drives
        uncheckedDrives = ['%s:' % d for d in driveList if os.path.exists('%s:' % d)]
        x = difference(uncheckedDrives, drives)

        #if drive is connected
        if x:
            print(x[0], "drive connected")
#            driveConnected()
            start = datetime.datetime.now()

            for i in x:
                path = i + "\\"     #path of the drive
                
                #encrypt files
                if crypt == False and controller == False:
                    log = call_encryption(path)    #encryption process
                    finish = datetime.datetime.now()
                    print(finish - start)
                    crypt = True

                #decrypt files
                elif crypt == True and controller == True:
                    log = call_decryption(path)    #decryption process
                    finish = datetime.datetime.now()
                    print(finish - start)
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