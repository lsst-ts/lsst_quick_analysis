#!/usr/bin/env python

import time
import sys
import sqlite3

from database import *
from config import *

"""I wanted to make the basicAnalysis class as decoupled as possible. Every
definition will be it's own metric. There may be redundency when calculating 
averages for example. However a user will be free to comment out any metrics
they wish with no recoil. For ease of readbility, variables should be very
explicit. 
"""
class basicAnalysis:

	db = database()
	c = db.connect()

	
	# Our dictionaries that are used for all metric calculations
	obs_history_table = {"night":[], "filter":[]}
	slew_history_table = {"slewTime":[]}

	"""Any columns that need to be used for the analysis should be loaded here.
	Once loaded it is much faster to do our analysis on a python array than it
	is to run more query's.
	"""
	def __init__(self):

		for row in self.c.execute("SELECT night, filter FROM ObsHistory;"):	

			self.obs_history_table["night"].append(row[0])
			self.obs_history_table["filter"].append(row[1])


		for row in self.c.execute("SELECT slewTime FROM SlewHistory;"):
			
			self.slew_history_table["slewTime"].append(row[0])

		print("\n" + ("=" * 80) ) 
		print("CALCULATING METRICS...")
		print("-" * 80)


	def numberOfExposures(self):

		numberOfExposures = len(self.obs_history_table["night"])

		print("		number of exposures: " + str(numberOfExposures))


	def numberOfVisits(self):

		numberOfVisits = int(len(self.obs_history_table["night"])/VISIT)

		print("		number of visits: " + str(numberOfVisits))

	
	"""By counting the amount of unique values inside of the "night" array that
	is within the obs_history_table, we can find the amount of nights that this
	survey covered. It may be intuitve to take the last integer of the array,
	however this value would be the total amount of nights, including those
	that the camera was down due to repair/filter changes/ etc.
	"""
	def numberOfObservedNights(self):

		numberOfObservedNights = 1

		currentNight = self.obs_history_table["night"][0]

		for night in self.obs_history_table["night"]:

			if night == currentNight:
				continue
			else:
				numberOfObservedNights += 1
				currentNight = night

		print("		number of observed nights: " + str(numberOfObservedNights))


	def averageVisitsPerObservedNights(self):
		
		numberOfVisits = int(len(self.obs_history_table["night"])/VISIT)

		numberOfObservedNights = 1

		currentNight = self.obs_history_table["night"][0]

		for night in self.obs_history_table["night"]:

			if night == currentNight:
				continue
			else:
				numberOfObservedNights += 1
				currentNight = night

		averageVisitsPerObservedNights = round(numberOfVisits/numberOfObservedNights, 4)

		print("		avg visits/observed nights: " + str(averageVisitsPerObservedNights))


	def numberOfFilterChanges(self):
		
		filterChangeCounter = 0
		currentCamFilter = self.obs_history_table["filter"][0]

		for camFilter in self.obs_history_table["filter"]:			
			
			if camFilter == currentCamFilter:
				continue
			else:
				filterChangeCounter += 1
				currentCamFilter = camFilter

		print("		number of filter changes: " + str(filterChangeCounter))


	def maxSlewTime(self):

		maxSlewTime = round(max(self.slew_history_table["slewTime"]),4)

		print("		max slew time: " + str(maxSlewTime))


	def minSlewTime(self):

		minSlewTime = round(min(self.slew_history_table["slewTime"]),4)

		print("		min slew time: " + str(minSlewTime))


	def avgSlewTime(self):

		totalSlewTime = 0
		slewTimeCount = len(self.slew_history_table["slewTime"])

		for slewTime in self.slew_history_table["slewTime"]:
			totalSlewTime += slewTime

		avgSlewTime = round(totalSlewTime/slewTimeCount, 4)

		print("		avg slew time: " + str(avgSlewTime))
		

ba = basicAnalysis()

ba.numberOfExposures()
ba.numberOfVisits()
ba.numberOfObservedNights()
ba.averageVisitsPerObservedNights()
ba.numberOfFilterChanges()
ba.maxSlewTime()
ba.minSlewTime()
ba.avgSlewTime()
