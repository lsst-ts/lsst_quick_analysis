# Absolute folder path that contains all your databases
DB_DIRECTORY = "/absolute/path/to/opsimDatabases/"

# Absolute folder path that contains all your logs
LOG_DIRECTORY = "/absolute/path/to/opsimLogs/"

# Folder path which reports are written into, optional
REPORT_DIRECTORY = "reports/"

# Python 2 & 3 compatible function binding
try:
   input = raw_input
except NameError:
   pass