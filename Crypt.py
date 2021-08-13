import time
import os.path
import datetime
from cryptography.fernet import Fernet

#find difference between list1 and list2...used here for finding newly connected or disconnected drive
def difference(list1, list2):
    list_difference = [item for item in list1 if item not in list2]
    return list_difference

def driveConnected():
    print("New drive connected")


def driveDisconnected():
    print("Drive disconnected")


#load key from current directory
def load_key():
    return open("key.key", "rb").read()


#encryption
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


#decryption
def decryption(filename, key):

    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()

        try:
            # decrypt data
            decrypted_data = f.decrypt(encrypted_data)
        except:
            print("Invalid token:\neither the file is not encrypted or some of its content has been modified")
        else:
            # write the original file
            with open(filename, "wb") as file:
                file.write(decrypted_data)


#driver code
if __name__ == '__main__':
    
    #list of possible drives
    driveList = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    drives = ['%s:' % d for d in driveList if os.path.exists('%s:' % d)]    #connected drives
    crypt = False
    controller = False       #to avoid encrpting an already encrypted drive
    print("connected drives:", drives)

    while True:

        #finding newly connected or disconnected drives
        uncheckedDrives = ['%s:' % d for d in driveList if os.path.exists('%s:' % d)]
        x = difference(uncheckedDrives, drives)

        #if drive is connected
        if x:
            print("New drives: " + str(x))
            driveConnected()
            current = datetime.datetime.now()

            for i in x:
                path = i + "\\"     #path of the drive
                
                #encrypt files
                if crypt == False and controller == False:

                    key = load_key()
                    for dirpath, dirnames, files in os.walk(path):
                        for file in files:
                            encryption(dirpath + "\\" + file, key)    #encryption process
                    print("files encrypted")
                    done = datetime.datetime.now()
                    print("time consumed: " + str(done - current))
                    crypt = True

                #decrypt files
                elif crypt == True and controller == True:

                    key = load_key()
                    for dirpath, dirnames, files in os.walk(path):
                        for file in files:
                            decryption(dirpath + "\\" + file, key)    #decryption process
                    print("files decrypted")
                    done = datetime.datetime.now()
                    print("time consumed: " + str(done - current) )
                    crypt = False

        x = difference(drives, uncheckedDrives)
        #if drive is disconnected
        if x:

            if controller:
                controller = False
            else:
                controller = True

            print("Removed drives: " + str(x))
            driveDisconnected()

        drives = ['%s:' % d for d in driveList if os.path.exists('%s:' % d)]

        time.sleep(1)

#shit