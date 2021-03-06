# Criptify
A python application that automatically encrypts and decrypts a USB flash drive

## Requirements
1. Python 3 (recommended version 3.9.0 or newer)
2. Cryptography package (recommended version 3.4.7 or newer)
3. Ray package (recommended version 1.6.0)

## Installation and Running
1. Go to [www.python.org](https://www.python.org/downloads/) and download the latest version of python if not already installed. You can verify python installation by typing "python -- version" in the command prompt/terminal.
2. Verify pip installation by entering "pip --version" in the command prompt.
3. Install [cryptography](https://pypi.org/project/cryptography/) package (easiest way is to enter "pip install cryptography").
4. Install [Ray](https://pypi.org/project/ray/) package (again the easiest way is "pip install ray")
4. Download the Cryptify source code. Open IDLE and open the source code you downloaded. Press F5 to run the script. Alternatively, you can run Criptify by opening cmd, changing the directory to where you saved Crypt.py and writing "python Crypt.py".
5. When running the program for the first time, first run GenerateKey.py to create an encryption key. Ignore this if the key has been already generated.
6. Insert a USB stick to start encrypting.

## How it works
After you run the application, inserting a USB drive will start encryption automatically. If you remove the drive and reinsert it, the decryption process will start and the drive will be decrypted. This application uses symmetric encryption technique. You should keep the encryption key safe to avoid permanent loss of data or unauthorised access.

## WARNING
Criptify is still a work in progress. There might be a chance of permanent encryption of data. Test the application on junk files before encrypting any sensitive information. Proceed with caution.

## Conclusion
In this project we developed an encryption and decryption application using Ray and cryptography library in python by employing AES. We found that after combining with Ray, the turnaround time of Criptify was reduced by almost 50%-75% on i5 7200U dual core processor. Using better processor would definitely decrease the turnaround time even further. In future work, we will add support for manual control, argument parsing, passwords, log files and using other encryption algorithms such as RSA, DESI, Blowfish, etc. 
