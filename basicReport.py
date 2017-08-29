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


	if not os.path.exists(directory):
		os.makedirs(directory)


	def writeOutBasicInfo(self):

		# file = open("reports/test.txt","w") 

		count = 0

		# for row in self.c.execute("SELECT SlewHistory.slewCount, SlewHistory.startDate, SlewHistory.endDate, SlewHistory.slewTime, SlewHistory.slewDistance, SlewInitialState.telAz AS startTelAz, SlewInitialState.telAlt AS startTelAlt, SlewInitialState.rotTelPos AS startRotTelPos, SlewInitialState.filter AS startFilter from SlewHistory, SlewInitialState"):
		for row in self.c.execute("SELECT SlewHistory.slewCount, SlewHistory.startDate, SlewHistory.endDate, SlewHistory.slewTime, SlewHistory.slewDistance, SlewInitialState.telAz AS startTelAz, SlewInitialState.telAlt AS startTelAlt, SlewInitialState.rotTelPos AS startRotTelPos, SlewInitialState.filter AS startFilter from SlewHistory JOIN SlewInitialState ON SlewHistory.slewCount = SlewInitialState.SlewHistory_slewCount JOIN SlewMaxSpeeds ON SlewInitialState.SlewHistory_slewCount = SlewMaxSpeeds.SlewHistory_slewCount"):
			if count == 10:
				break
			count += 1
			print(row)



br = basicReport()

br.writeOutBasicInfo()