#!/usr/bin/env python

import sqlite3
import os

from database import *


class basicReport:

	db = database()
	c = db.connect()
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'
	directory = "reports/"

	# Printing "parts"

	LINE = "+-----------+------------------+------------------+------------+------------+------------+-------------+----------------+-------------+"
	HEADER = "| slewCount | startDate        | endDate          | slewTime   |  slewDist  | startTelAz | startTelAlt | startRotTelPos | startFilter |"

	if not os.path.exists(directory):
		os.makedirs(directory)


	def writeOutBasicInfo(self):

		file = open("reports/test.txt","w") 

		file.write(self.LINE + "\n")
		file.write(self.HEADER + "\n")
		file.write(self.LINE + "\n")


		count = 0

		for row in self.c.execute("""SELECT SlewHistory.slewCount, 
											SlewHistory.startDate, 	
											SlewHistory.endDate, 
											SlewHistory.slewTime, 
											SlewHistory.slewDistance, 
											SlewInitialState.telAz AS startTelAz, 
											SlewInitialState.telAlt AS startTelAlt, 
											SlewInitialState.rotTelPos AS startRotTelPos, 
											SlewInitialState.filter AS startFilter FROM SlewHistory 
											JOIN SlewInitialState ON SlewHistory.slewCount = SlewInitialState.SlewHistory_slewCount"""):
			
			file.write('|{:>10} | {:>16} | {:>16} | {:>10} | {:>10} | {:>10} | {:>11} | {:>14} | {:>11} |'
				.format(str(row[0]), str(row[1]), str(row[2]), str(round(row[3],6)), str(round(row[4],6)), str(round(row[5],6)), str(round(row[6],6)), str(round(row[7],6)), str(row[8]) ) )


			file.write("\n") 




			if count == 10:
				break
			count += 1
			

br = basicReport()

br.writeOutBasicInfo()