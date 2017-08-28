#!/usr/bin/env python

import sqlite3
from database import *

class basicAnalysis:

	db = database()
	c = db.connect()

	def visitePerNight(self):

		count = 0
		print("Calculating Visits Per Night...")

		for row in self.c.execute("SELECT paramName FROM Config  ASC LIMIT 0, 900000;"):
			print(row)
			count+=1

		print("Total: " + str(count))



ba = basicAnalysis()
ba.visitePerNight()
