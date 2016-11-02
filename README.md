## pipl_test

#Summary 

	- Loop over HTML files 
	- Parse them using LXML
	- Extract properties using XPATHs
	- Parse them into JSON object  
	- Keep Statistics of all pages & fields extracted 

###All records can be found under 'out' folder. 
###Statistics - can be found in the 'out' folder under "Statistics.json" 

####** Since Locality was asked in a city/state/country - I had to use geocoder in order to extract properly.
#### The down-side of that is latency. (Normally I wouldn't use it). 
