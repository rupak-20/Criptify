# Criptify
A python application that automatically encrypts and decrypts a USB flash drive

## Requirements
1. Python 3 (recommended version 3.9.0 or newer)
2. Cryptography package (recommended version 3.4.7 or newer)

## Installation and Running
1. Go to https://www.python.org/downloads/ and download the latest version of python if not already installed. You can verify python installation by typing "python -- version" in command prompt in windows machines.
2. Verify pip installation by entering "pip --version" in command prompt (again if you are using windows).
3. Install [cryptography] (https://pypi.org/project/cryptography/) package (easiet way is to enter "pip install cryptography" in cmd).
4. Download the Cryptify source code. Open IDLE and open the source code you downloaded. Press F5 to run the script. Alternatively you can run Criptify by opening cmd, changing the directory to where you saved crypt.py and writing "python Crypt.py".
5. When you are running the program for the first time, first run GenerateKey.py to create an enryption key. Ignore this if key has been already generated.
6. Insert a USB stick to start encrypting.

## How it works
After you run the application, inserting a USB drive will start encryption automatically. If you remove the drive and reinsert it, the decryption process will start and drive will be decrypted. This application uses symmetric encryption technique. You should keep the encryption key safe to avoid permanent loss of data or unauthorised access.

## WARNING
Criptify is still a work in progress. There might be a chance of permanent encryption of data. Test the application on junk files before encrypting any sensitive information. Proceed with caution.
