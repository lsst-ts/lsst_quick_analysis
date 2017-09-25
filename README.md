# Purpose

"lsst_quick_analysis" is a tool used to produce various metrics to helps users
do quick analysis on OpSim4 output.


### How to use

1) Do `cp configTemplate.py config.py`

2) Modify the `DB_DIRECTORY` variable inside of `config.py`

3) Do `./[script]` on any of the scripts you wish to run



### Available scripts

`./basicAnalysis.py [run #]`: Prints to stdout a summary of varius values (averages, min, max etc.) An example run of "collosus_2177.db" could be `./basicAnalysis 2177`. This command would analyse the first file found with the 2177 appendage.

`./basicReport.py`: Writes out to a file useful columns in a human readable table


