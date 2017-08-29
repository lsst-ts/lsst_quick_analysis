#!/usr/bin/env python

import time
import sys
import sqlite3

from database import *

class basicAnalysis:

	db = database()
	c = db.connect()
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'

	def numberOfNights(self):
		
		print("Calculating number of nights...")

		count = 0
		for row in self.c.execute("SELECT * FROM ObsExposures;"):			
			count+=1

		print(self.CURSOR_UP_ONE + self.ERASE_LINE + "Calculating number of nights... " + str(count))


	def visitePerNight(self):
		
		print("Calculating visits per night...")
		
		count = 0
		for row in self.c.execute("SELECT * FROM ObsExposures;"):			
			count+=1

		print(self.CURSOR_UP_ONE + self.ERASE_LINE + "Calculating visits per night... " + str(count/2))

	def visitsPerNightAvg(self):

		print("Calculating visits per night avg...")

		counter = {}
		total = 0

		for row in self.c.execute("SELECT night FROM ObsHistory;"):			
			
			night = row[0]
			total += 1

			if night in counter:
				counter[night] = counter[night] + 1
			else:
				counter[night] = 1

			avg = total/len(counter)

		print(self.CURSOR_UP_ONE + self.ERASE_LINE + "Calculating visits per night avg... " + str(avg))

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

	def filterChangesPerNightAvg(self):
		print("Calculating total filter changes per night avg... ")

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

	def parkPositionsTaken():
		pass




ba = basicAnalysis()

ba.numberOfNights()
ba.visitePerNight()
ba.visitsPerNightAvg()
ba.totalFilterChanges()
ba.slewTimeNumbers()
