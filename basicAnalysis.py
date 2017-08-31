#!/usr/bin/env python

import time
import sys
import sqlite3

from database import *
from config import *

class basicAnalysis:

	db = database()
	c = db.connect()
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'


	def nightNumbers(self):
		
		print("Calculating night numbers...")

		totalNightCount = 0
		visitsPerNightCounter = {}


		# Get the total amount of exposures, as well as how many nights these exposure count for
		for row in self.c.execute("SELECT night FROM ObsHistory;"):			
			
			totalNightCount+=1
			currNight = row[0]

			if currNight in visitsPerNightCounter:
				visitsPerNightCounter[currNight] = visitsPerNightCounter[currNight] + 1
			else:
				visitsPerNightCounter[currNight] = 1

		totalVisitCount = totalNightCount/VISIT

		print("		number of nights: " + str(totalNightCount))
		print("		number of visits: " + str(totalVisitCount))
		print("		visits/night avg: " + str(totalVisitCount/(len(visitsPerNightCounter))))



	def totalFilterChanges(self):

		print("Calculating total filter changes... ")

		counter = 0
		curs = self.c.execute("SELECT filter FROM ObsHistory;")
		currentFilter = curs.fetchone()[0]


		for row in self.c.execute("SELECT filter FROM ObsHistory;"):			
			
			if currentFilter == row[0]:
				continue
			else:
				counter += 1
				currentFilter = row[0]

		print(self.CURSOR_UP_ONE + self.ERASE_LINE + "Calculating total filter changes... " + str(counter))


	def slewTimeNumbers(self):

		print("Calculating slew time numbers...")

		# for calculating avg
		totalSlewTimes = 0
		totalSlewTime = 0

		# starting val for calculating min & max
		curs = self.c.execute("SELECT slewTime FROM SlewHistory;")
		maxVal = curs.fetchone()[0]
		minVal = maxVal

		for row in self.c.execute("SELECT slewTime FROM SlewHistory;"):			
			slewTime = row[0]
			totalSlewTimes += 1
			totalSlewTime += slewTime

			if slewTime < minVal:
				minVal = slewTime

			if slewTime > maxVal:
				maxVal = slewTime

		slewAverage = totalSlewTime/totalSlewTimes

		print("		avg: " + str(slewAverage))
		print("		min: " + str(minVal))
		print("		max: " + str(maxVal))



ba = basicAnalysis()

ba.nightNumbers()
# ba.totalFilterChanges()
ba.slewTimeNumbers()