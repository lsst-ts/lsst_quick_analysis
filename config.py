# The location you wish the scripts to write files into
REPORT_DIRECTORY = "reports/"

# The folder that contains all your databases
DB_DIRECTORY = "/Users/aheyer/Projects/OpSimDB/"

# Python 2 & 3 compatible function binding
try:
   input = raw_input
except NameError:
   pass
