#!/usr/bin/env python

import sqlite3
import os

from config import *
from database import *


class basicReport:

	# Some pre-liminary set up for the run
	db = database()
	c = db.connect()
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'
	if not os.path.exists(REPORT_DIRECTORY):
		os.makedirs(REPORT_DIRECTORY)

	# Printing "parts" 
	LINE = "+-----------+------------------+------------------+--------------+--------------+--------------+--------------+--------------+--------------+"
	HEADER_START = "| slewCount | startDate        | endDate          | slewTime     |  slewDist    | startTelAz   | startTelAlt  |startRotTelPos| startFilter  |"
	HEADER_FINAL = "| slewCount | startDate        | endDate          | slewTime     |  slewDist    | finalTelAz   | finalTelAlt  |finalRotTelPos| finalFilter  |"

	def writeOutStartSlewInfo(self):

		file = open("reports/initSlewInfo.txt","w") 

		file.write(self.LINE + "\n")
		file.write(self.HEADER_START + "\n")
		file.write(self.LINE + "\n")

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
			
			file.write('|{:>10} | {:>16} | {:>16} | {:>12} | {:>12} | {:>12} | {:>12} | {:>12} | {:>12} |\n'
				.format(str(row[0]), str(round(row[1],2)), str(round(row[2],2)), str(round(row[3],6)), str(round(row[4],6)), 
						str(round(row[5],6)), str(round(row[6],6)), str(round(row[7],6)), str(row[8])))

		
	def writeOutFinalSlewInfo(self):

		file = open("reports/finalSlewInfo.txt","w") 

		file.write(self.LINE + "\n")
		file.write(self.HEADER_FINAL + "\n")
		file.write(self.LINE + "\n")

		for row in self.c.execute("""SELECT SlewHistory.slewCount, 
											SlewHistory.startDate, 	
											SlewHistory.endDate, 
											SlewHistory.slewTime, 
											SlewHistory.slewDistance, 
											SlewFinalState.telAz AS finalTelAz, 
											SlewFinalState.telAlt AS finalTelAlt, 
											SlewFinalState.rotTelPos AS finalRotTelPos, 
											SlewFinalState.filter AS finalFilter FROM SlewHistory 
											JOIN SlewFinalState ON SlewHistory.slewCount = SlewFinalState.SlewHistory_slewCount"""):
			
			file.write('|{:>10} | {:>16} | {:>16} | {:>12} | {:>12} | {:>12} | {:>12} | {:>12} | {:>12} |\n'
				.format(str(row[0]), str(round(row[1],2)), str(round(row[2],2)), str(round(row[3],6)), str(round(row[4],6)), 
						str(round(row[5],6)), str(round(row[6],6)), str(round(row[7],6)), str(row[8])))


br = basicReport()
br.writeOutStartSlewInfo()
br.writeOutFinalSlewInfo()