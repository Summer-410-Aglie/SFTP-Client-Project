# sftp test

# Unit test

# To perform unit test, you can type this command python -m unittest 'tests/test_sftp_client.py'

# Steps for setting up WSL
### If you're having issues at any point in this process, restarting/refreshing VSCode or your computer is likely to help
1. Search for "Turn Windows features on or off"
2. Scroll down and check the tick box for "Windows Subsystem for Linux"
3. Restart computer
4. Download Ubuntu from Microsoft Store (4.4 star average rating, from Canonical Group Ltd)
5. I'm honestly not sure which are required and which aren't but in the Ubuntu terminal,
	I eventually ran all of these in this order:
	* `sudo apt install python3-dev`
	* `sudo apt update`
	* `sudo apt upgrade`
	* `sudo apt install python3-pip`
6. In the Ubuntu terminal, `cd` into the directory where this project is
7. Type `code .` to open this in VSCode (you will have to download Microsoft's `WSL`
	extension in VSCode for it to work)
8. Delete your `.venv` folder and recreate the environment using the `requirements.txt`