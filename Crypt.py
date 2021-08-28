import ray
import time
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
def encryption(filename, key):

    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()

        # encrypt data
        encrypted_data = f.encrypt(file_data)

        # write the encrypted file
        with open(filename, "wb") as file:
            file.write(encrypted_data)

    return filename


#decryption
@ray.remote
def decryption(filename, key, skipped):

    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()

        try:
            # decrypt data
            decrypted_data = f.decrypt(encrypted_data)
        except:
            skipped.append(filename)
        else:
            # write the original file
            with open(filename, "wb") as file:
                file.write(decrypted_data)

    return filename


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

                    encrypted_files = []
                    print("encrypting files...")

                    for dirpath, dirnames, files in os.walk(path):
                        for file in files:
                            encrypted_files.append(encryption.remote(dirpath + "\\" + file, key))    #encryption process
                    encrypted_files = ray.get(encrypted_files)

                    print("encrypted", len(encrypted_files), "files")
                    print("encryption completed")
                    end = time.time()
                    print("time consumed: ", end - start)
                    crypt = True

                #decrypt files
                elif crypt == True and controller == True:

                    decrypted_files = []
                    modified_or_invalid_files = []
                    print("decrypting files...")

                    for dirpath, dirnames, files in os.walk(path):
                        for file in files:
                            decrypted_files.append(decryption.remote(dirpath + "\\" + file, key, modified_or_invalid_files))    #decryption process
                    decrypted_files = ray.get(decrypted_files)

                    if len(modified_or_invalid_files) > 0:
                        print("skipped", len(modified_or_invalid_files), "files")
                        print("files were either invalid for decryption or modified previously")
                    print("decrypted", len(decrypted_files), "files")
                    print("decryption completed")
                    end = time.time()
                    print("time consumed: ", end - start)
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
    #support enctyption of large files
    #create a dedicated website
    #containerize the app using docker
    #create and distribute executables and docker images
    #add support for log files
    #add RSA encryption
    #(maybe) add GUI