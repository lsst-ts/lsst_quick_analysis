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
explicit. If variable names contains an underscore, then I am refering to 
database schema related attributes.
"""
class basicAnalysis:

	db = database()
	c = db.connect()

	
	# Our dictionaries where all metric calculations derive from
	obs_history_table = {"observationId": [],"night":[], "filter":[]}
	obs_proposal_history_table = {"propHistId":[], "proposal_propId":[], "obsHistory_observationId":[]}
	slew_history_table = {"slewTime":[]}

	"""Any columns that need to be used for the analysis should be loaded here.
	Once loaded it is much faster to do our analysis on a python array than it
	is to run more query's.
	"""
	def __init__(self):

		print("\n" + ("=" * 80) ) 
		print("CALCULATING METRICS...")
		print("-" * 80)


		for row in self.c.execute("SELECT observationId, night, filter FROM ObsHistory;"):	

			self.obs_history_table["observationId"].append(row[0])
			self.obs_history_table["night"].append(row[1])
			self.obs_history_table["filter"].append(row[2])

		for row in self.c.execute("SELECT propHistId, Proposal_propId, ObsHistory_observationId FROM ObsProposalHistory;"):
			
			self.obs_proposal_history_table["propHistId"].append(row[0])
			self.obs_proposal_history_table["proposal_propId"].append(row[1])
			self.obs_proposal_history_table["obsHistory_observationId"].append(row[2])

		for row in self.c.execute("SELECT slewTime FROM SlewHistory;"):
			
			self.slew_history_table["slewTime"].append(row[0])

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

	def avgFilterChangesPerNight(self):

		filterChangeCounter = 0
		currentCamFilter = self.obs_history_table["filter"][0]

		for camFilter in self.obs_history_table["filter"]:			
			
			if camFilter == currentCamFilter:
				continue
			else:
				filterChangeCounter += 1
				currentCamFilter = camFilter

		numberOfObservedNights = 1

		currentNight = self.obs_history_table["night"][0]

		for night in self.obs_history_table["night"]:

			if night == currentNight:
				continue
			else:
				numberOfObservedNights += 1
				currentNight = night

		avgFilterChangesPerNight = filterChangeCounter/numberOfObservedNights

		print("		avg filer changes/observed nights: " + str(round(avgFilterChangesPerNight,2)))


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


		# Python 2 needs floats, otherwise 2/3 = 0
		histVisitCount *= 1.0
		visitCount *= 1.0

		
		# Visit count of each proposal
		NES = historyProposalCounter[1]/VISIT
		SCP = historyProposalCounter[2]/VISIT
		WFD = historyProposalCounter[3]/VISIT
		GP = historyProposalCounter[4]/VISIT
		DD = historyProposalCounter[5]/VISIT


		NES_prop_hist_perc = (NES/histVisitCount) * 100
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


	# Because we load only tables and thier corresponding, it is redundent to do another quary.
	# Rather than using a costly quary's we do something similiar to a sql "join". I use an index
	# based array on the proposal_proId column of the schema, then from there use the index I am on
	# to derive what filter it corresponds to on the other columns.  
	def numberOfVisitsInEachFilterPerProposal(self):
		

		numberOfVisitsPerFilterPerProposal = {}

		# Our columns that we will need to traverse to calculate this metric
		obs_proposal_history_propId_col = self.obs_proposal_history_table["proposal_propId"]
		obs_proposal_history_obsHistoryId_col = self.obs_proposal_history_table["obsHistory_observationId"]
		obs_history_filter_col = self.obs_history_table["filter"]


		for i in range(len(obs_proposal_history_propId_col)):


			# if i == 132:
			# 	break

			proposalId = obs_proposal_history_propId_col[i]

			# Our arrays start at 0, the unique id's we derive indexes from do not			
			indexToObsHistory = obs_proposal_history_obsHistoryId_col[i]-1

			filterForThisProposal = obs_history_filter_col[indexToObsHistory]

			# If the proposal already exists in our dictionary
			if proposalId in numberOfVisitsPerFilterPerProposal:
				
				# AND if the the filter exists in that then increment its count
				if filterForThisProposal in numberOfVisitsPerFilterPerProposal[proposalId]:
					numberOfVisitsPerFilterPerProposal[proposalId][filterForThisProposal] += 1

				# If the filter does not exist create it and set it to 1
				else:
					numberOfVisitsPerFilterPerProposal[proposalId][filterForThisProposal] = 1

			# If the proposal is not in the dictinary, add it along with its filter set to 1
			else:
				numberOfVisitsPerFilterPerProposal[proposalId] = {}
				numberOfVisitsPerFilterPerProposal[proposalId][filterForThisProposal] = 1

		
		# The lists in the block below MUST be the same length for out loop logic to work
		FILTERS = ["z", "y", "i", "r", "g", "u"]
		NES = [0, 0, 0, 0, 0, 0]
		SCP = [0, 0, 0, 0, 0, 0]
		WFD = [0, 0, 0, 0, 0, 0]
		GP = [0, 0, 0, 0, 0, 0]
		DD = [0, 0, 0, 0, 0, 0]
	

		# Remember that the hard coded 1,2,3,4,5 correspond to the proposal id's from the db schema
		for i in range(len(NES)):

			try:
				NES[i] = numberOfVisitsPerFilterPerProposal[1][FILTERS[i]]
			except Exception:
				pass

			try:
				WFD[i] = numberOfVisitsPerFilterPerProposal[2][FILTERS[i]]
			except Exception:
				pass

			try:
				SCP[i] = numberOfVisitsPerFilterPerProposal[3][FILTERS[i]]
			except Exception:
				pass

			try:
				GP[i] = numberOfVisitsPerFilterPerProposal[4][FILTERS[i]]
			except Exception:
				pass

			try:
				DD[i] = numberOfVisitsPerFilterPerProposal[5][FILTERS[i]]
			except Exception:
				pass


		print("		{:>18}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}".format(" ", "z", "y", "i", "r", "g", "u"))
		print("		NorthElipticSpur  : {:>6}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}".format( *NES ) )
		print("		SouthCelestialPole: {:>6}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}".format( *SCP ) )
		print("		WideFastDeep      : {:>6}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}".format( *WFD ) )
		print("		GalacticPlane     : {:>6}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}".format( *GP ) )
		print("		DeepDrilling      : {:>6}  {:>6}  {:>6}  {:>6}  {:>6}  {:>6}".format( *DD ) )



ba = basicAnalysis()

ba.numberOfExposures()
ba.numberOfVisits()
ba.numberOfObservedNights()
ba.averageVisitsPerObservedNights()

print("")

ba.numberOfFilterChanges()
ba.avgFilterChangesPerNight()

print("")

ba.maxSlewTime()
ba.minSlewTime()
ba.avgSlewTime()

print("")

ba.numberOfVisitsPerProposal()

print("")

ba.numberOfVisitsInEachFilterPerProposal()
