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

	
	# Our dictionaries where all metric calculations derive from
	obs_history_table = {"night":[], "filter":[]}
	obs_proposal_history_table = {"proposal_propId":[]}
	slew_history_table = {"slewTime":[]}

	"""Any columns that need to be used for the analysis should be loaded here.
	Once loaded it is much faster to do our analysis on a python array than it
	is to run more query's.
	"""
	def __init__(self):

		print("\n" + ("=" * 80) ) 
		print("CALCULATING METRICS...")
		print("-" * 80)


		for row in self.c.execute("SELECT night, filter FROM ObsHistory;"):	

			self.obs_history_table["night"].append(row[0])
			self.obs_history_table["filter"].append(row[1])

		for row in self.c.execute("SELECT slewTime FROM SlewHistory;"):
			
			self.slew_history_table["slewTime"].append(row[0])

		for row in self.c.execute("SELECT Proposal_propId FROM ObsProposalHistory;"):

			self.obs_proposal_history_table["proposal_propId"].append(row[0])

		# for row in self.c.execute("SELECT propId FROM Proposal;"):

		# 	# 1 = NorthElipticSpur
		# 	# 2 = SouthCelestialPole
		# 	# 3 = WideFastDeep
		# 	# 4 = GalacticPlance
		# 	# 5 = DeepDrilling
		# 	self.proposal_table[row[0]] = 0


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


	""" These arbitrary numbers are decided by the scientists, noted here a
	second time for easy reference on the print statements. 
	1 = NorthElipticSpur (NES)
	2 = SouthCelestialPole (SCP)
	3 = WideFastDeep (WFD)
	4 = GalacticPlane (GP)
	5 = DeepDrilling (DD)

	I list two percents, one divided by "history visit count" which is the 
	totaled number of visits in each proposal. The other is "visit count" which
	is the actual number of visits the physical telescope made
	"""
	def numberOfVisitsPerProposal(self):


		# get the total amount of proposals found
		histVisitCount = 0
		historyProposalCounter = {}
		
		for each in self.obs_proposal_history_table["proposal_propId"]:
			
			histVisitCount += 1

			if each in historyProposalCounter:
				historyProposalCounter[each] += 1
			else:
				historyProposalCounter[each] = 1


		# hist visit count given our def of VISIT, may be more than the 
		# number of actual visits since there may be overlap in proposals
		histVisitCount/=VISIT
		visitCount = int(len(self.obs_history_table["night"])/VISIT)
		
		# Visit count of each proposal
		NES = historyProposalCounter[1]/VISIT
		SCP = historyProposalCounter[2]/VISIT
		WFD = historyProposalCounter[3]/VISIT
		GP = historyProposalCounter[4]/VISIT
		DD = historyProposalCounter[5]/VISIT

		NES_prop_hist_perc = NES/histVisitCount * 100
		SCP_prop_hist_perc = SCP/histVisitCount * 100
		WFD_prop_hist_perc = WFD/histVisitCount * 100
		GP_prop_hist_perc = GP/histVisitCount * 100
		DD_prop_hist_perc = DD/histVisitCount * 100
		total_prop_hist_perc = round(NES_prop_hist_perc + SCP_prop_hist_perc + WFD_prop_hist_perc + GP_prop_hist_perc + DD_prop_hist_perc,2)

		NES_prop_perc = NES/visitCount * 100
		SCP_prop_perc = SCP/visitCount * 100
		WFD_prop_perc = WFD/visitCount * 100
		GP_prop_perc = GP/visitCount * 100
		DD_prop_perc = DD/visitCount * 100
		total_prop_perc = round(NES_prop_perc + SCP_prop_perc + WFD_prop_perc + GP_prop_perc + DD_prop_perc,2)


		print("		{:>42}  {:>10}".format("(history)", "(total)"))
		print("		NorthElipticSpur  : {:>10} {:>10}% {:>10}%".format(str(round(NES,2)), str(round(NES_prop_hist_perc,2)), str(round(NES_prop_perc,2))))
		print("		SouthCelestialPole: {:>10} {:>10}% {:>10}%".format(str(round(SCP,2)), str(round(SCP_prop_hist_perc,2)), str(round(SCP_prop_perc,2))))
		print("		WideFastDeep      : {:>10} {:>10}% {:>10}%".format(str(round(WFD,2)), str(round(WFD_prop_hist_perc,2)), str(round(WFD_prop_perc,2))))
		print("		GalacticPlane     : {:>10} {:>10}% {:>10}%".format(str(round(GP,2)) , str(round(GP_prop_hist_perc,2)) , str(round(GP_prop_perc,2))))
		print("		DeepDrilling      : {:>10} {:>10}% {:>10}%".format(str(round(DD,2)) , str(round(DD_prop_hist_perc,2)) , str(round(DD_prop_perc,2))))
		print("		{:>42}% {:>10}%".format(total_prop_hist_perc, total_prop_perc))




ba = basicAnalysis()

ba.numberOfExposures()
ba.numberOfVisits()
ba.numberOfObservedNights()
ba.averageVisitsPerObservedNights()

print()

ba.numberOfFilterChanges()

print()

ba.maxSlewTime()
ba.minSlewTime()
ba.avgSlewTime()

print()

ba.numberOfVisitsPerProposal()
