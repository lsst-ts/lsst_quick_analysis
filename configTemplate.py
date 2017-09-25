# Folder path that contains all your databases
DB_DIRECTORY = "/path/to/opsimDatabases/"

# Folder path which reports are written into 
REPORT_DIRECTORY = "reports/"

# Python 2 & 3 compatible function binding
try:
   input = raw_input
except NameError:
   pass
