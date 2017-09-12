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
either a whole table, or just a column form the database schema.
"""
class basicAnalysis:

	db = database()
	c = db.connect()
	
	# Our dictionaries where all metric calculations derive from
	obs_history_table = {"observationId": [],"night":[], "filter":[]}
	obs_proposal_history_table = {"propHistId":[], "proposal_propId":[], "obsHistory_observationId":[]}
	slew_history_table = {"slewTime":[]}

	"""Any columns that needs to be used for the analysis should be loaded here.
	Once loaded it is much faster to do our analysis on a python array than it
	is to run more query's. Some columns, such as id's to other tables are also
	needed for python equivilent of sql "joins". 
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


		# Check to see if our tables have data, exit if not
		if len(self.obs_history_table["night"]) == 0:
			print("This table seems to have no recorded visits, exiting")
			sys.exit()


	def numberOfVisits(self):

		numberOfVisits = len(self.obs_history_table["night"])

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
		
		numberOfVisits = len(self.obs_history_table["night"]) * 1.0

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


	""" These arbitrary numbers are decided by the scientists, noted here for 
	easy reference on the print statements. 
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

		numberOfVisits = len(self.obs_history_table["night"])

		historyProposalCounter = { 1:0, 2:0, 3:0, 4:0, 5:0 }
		
		# get the total amount of exposures made on behalf of a proposal, note
		# that some visits can count for more than 1 proposal
		for each in self.obs_proposal_history_table["proposal_propId"]:
			
			# Grab the amount PER proposal
			if each in historyProposalCounter:
				historyProposalCounter[each] += 1
			else:
				historyProposalCounter[each] = 1


		# Python 2 float conversion, otherwise 2/3 = 0
		numberOfVisits *= 1.0
		
		# Visit count of each proposal
		NES = historyProposalCounter[1] * 1.0
		SCP = historyProposalCounter[2] * 1.0
		WFD = historyProposalCounter[3] * 1.0
		GP = historyProposalCounter[4] * 1.0
		DD = historyProposalCounter[5] * 1.0
		total_prop_hist = NES + SCP + WFD + GP + DD

		# Percent of each proposal reletaive to the total amount of vists
		# made on behalf of a proposal. Remember, may be over 100% totaled since
		# some visits can count for two proposals. 
		NES_prop_hist_perc = (NES/numberOfVisits) * 100
		SCP_prop_hist_perc = (SCP/numberOfVisits) * 100
		WFD_prop_hist_perc = (WFD/numberOfVisits) * 100
		GP_prop_hist_perc = (GP/numberOfVisits) * 100
		DD_prop_hist_perc = (DD/numberOfVisits) * 100
		total_prop_hist_perc = round(NES_prop_hist_perc + SCP_prop_hist_perc + WFD_prop_hist_perc + GP_prop_hist_perc + DD_prop_hist_perc,4)

		print("		NorthElipticSpur  : {:>10} {:>10}%".format(str(round(NES,4)), str(round(NES_prop_hist_perc,4))))
		print("		SouthCelestialPole: {:>10} {:>10}%".format(str(round(SCP,4)), str(round(SCP_prop_hist_perc,4))))
		print("		WideFastDeep      : {:>10} {:>10}%".format(str(round(WFD,4)), str(round(WFD_prop_hist_perc,4))))
		print("		GalacticPlane     : {:>10} {:>10}%".format(str(round(GP,4)) , str(round(GP_prop_hist_perc,4))))
		print("		DeepDrilling      : {:>10} {:>10}%".format(str(round(DD,4)) , str(round(DD_prop_hist_perc,4))))
		print("		" + "-"*42)
		print("		Total             : {:>10} {:>10}%".format(total_prop_hist, total_prop_hist_perc))


	"""Because we load only tables and reduce run time by limiting our sql calls,
	we do a python equivilent of a sql "join". The explicit naming convention is
	meant to clarify any ambiguity. Essentially we are grabbing values from one 
	column from one to be able to retrieve a value from a different tables column.  
	"""  
	def numberOfVisitsInEachFilterPerProposal(self):
		
		# Will look something like {"proposal Id" : {"filter Id" : "count"} }
		numberOfVisitsPerFilterPerProposal = {}

		# Our columns that we will need to traverse to calculate this metric
		obs_proposal_history_propId_col = self.obs_proposal_history_table["proposal_propId"]
		obs_proposal_history_obsHistoryId_col = self.obs_proposal_history_table["obsHistory_observationId"]
		obs_history_filter_col = self.obs_history_table["filter"]

		# Let's check to make sure our index which point to another table, actually exists in that table.
		# In other words, make sure we won't get an index out of bounds.
		if obs_proposal_history_obsHistoryId_col[-1] > len(obs_history_filter_col):
			print("		This DB seems to have foriegn keys in the ObsProposalHistory")
			print("		table which do not exist in the ObsProposalHistory table,")
			print("		therefore cannot compute the number of visits in each filter")
			print("		per proposal, skipping this metric")
			return

		# Start by itertating through all exposures made on behalf of a proposal,
		# may be more than the amount of exposures physically made since one exposure
		# can count for more than one proposal
		for i in range(len(obs_proposal_history_propId_col)):

			proposalId = obs_proposal_history_propId_col[i]

			# Our arrays start at 0, the unique id's we derive indexes from do not, 
			# so subtract 1 to accomodate for this caveat			
			indexToObsHistory = obs_proposal_history_obsHistoryId_col[i]-1

			# Retieve the filter which is in another table that was made on behalf of this exposure
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