import os
import sys
import sqlite3

from config import *


"""The database class is responsible for configuring all database related tasks.
This includes connection to "*.db" files and exposing it's database related 
resources to outside classes, for example a cursor. 
"""
class database:

	files = [f for f in os.listdir(DB_DIRECTORY) 
		if os.path.isfile(os.path.join(DB_DIRECTORY, f)) and ".db" in f]

	# Create a string friendly list of files found in DB_DIRECTORY
	allFiles = ""
	for each in files:
		if len(allFiles.split("\n")[-1] + each) > 80:
			allFiles += "\n"

		allFiles += each + ", "

	# Make this public path avilable to other classes
	path = ""

	"""Creates a cursor to a database to be used within the other scripts. Also
	responsible for printing out useful information to the user along with 
	obtaining the file that the user wishes to analyse
	"""
	def connect(self):

		if len(sys.argv) > 2:

			print("Can only be ran with 1 or no arguments, ex; `./basicAnalysis 2177` will execute the script on the first file named `*_2177` within the `DB_DIRECTORY` specified in `config.py` ")

		if len(sys.argv) == 2:

			print(sys.argv[1])

		else:

			print("=" * 80)
			print("Found [" + str(len(self.files)) + "] databases inside of '" + DB_DIRECTORY + "'")
			print("-" * 80)
			print('%5s' % self.allFiles)
			print(("=" * 80) +"\n")

			databaseFile = str(input('Please type the name of the database you wish to analyze: '))
			
			while True:

				if databaseFile in self.files:
					break
				else:
					print("\n" + ("-"* 80))
					print("!!! Could not find '" + databaseFile + "' inside of '" + DB_DIRECTORY + "' !!!")
					print(("-" *80) + "\n")

					databaseFile = str(input('try again: '))


			self.path = DB_DIRECTORY + databaseFile
			conn = sqlite3.connect(self.path)
			curs = conn.cursor()	
			return curs