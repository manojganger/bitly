# bitly
This is the exercise to read csv and json files and transform the data using Pandas


### First Step to install and run this program.
1. git clone <url> (clone the repo in your desired folder)

2. On windows machine :rightclick and select run powershell setvirenv.ps1 and click (that's it)
	
	the powershell script will check the python version 3 (or else will install it). 
	then dependencies will be installed if needed.
	copy the source code into the virtual env and 
	execute it and 
	the output will be produced on the console and pause the screen and
	then deactivate it.

## Dependencies
	pandas, pylint and pytest are the packages which are installed as per the powershell script.
	
## Design considerations
	The methods are logically grouped together like 
	1. reading config files then
	2. reading the data files then 
	3. analysing the data and then
	4. displaying the data as per the ask
	
	5. duplicate check is performed only on encodes.csv as it should be unique to avoid many to many join
	6. As there can be many test cases to test the code and the data files, few are implemented but it is separated out for more additions.
	7. All the code is on the top folder, data files are in data folder, configuration file is in config folder and the test cases are in test folder
	8. config.ini can contain more keys for the parameters which can be used in the code. This will avoid modifying the code for each of these parameter change.
	e.g chunk_size can be increased and decreased to see the best performing value for the execution.
	9. The code is timed for the #of seconds it took for execution. This would help in improving the performance by changing the chunk_size in config.ini file.
	10. Only the encoded hash keys are taken for the analysis. This is as per design as to include others, just add the line in the encodes.csv and it will be picked by the program.
