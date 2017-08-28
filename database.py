import sqlite3

class database:

	path = '/Users/aheyer/Projects/mafDevelopment/test1/colossus_2177.db'
	conn = sqlite3.connect(path)

	def connect(self):
		curs = self.conn.cursor()	
		return curs