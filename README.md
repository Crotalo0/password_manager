# password_manager
Python tkinter password manager.
Because of how environment variables are stored by the program, currently works only on linux.

Usage:
FIRST ACCESS:
Generate an encryption KEY, will be sotred in "my_key.key".
load the key, set a master password, it will be encrypted and stored as an env variable in .bashrc.
select a website, enter id/email, enter password, click add.

for next access just click load encryption key.
Make sure that my_key.key is in the same dir.

To see saved passwords:
Enter site for which password is needed, clich search, enter master password.

Password are encrypted with fernet library and saved in a .json file in working directory.
