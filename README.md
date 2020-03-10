# Dev-Parser
 
This project is intended to help process deviations for quality control purposes in a very specific setting. In short, it takes a csv input and looks for a specific column, in this case the column contains 1+ employee names. The number of rows each employee apears on is tallied and output to summary file. Then an excel workbook is output with a sheet for each employee and a list of the rows their name appeared on. 

Copy the files to a directory you are not likely to delete (your user home folder might be a good place). Modify the bat file to point to your location for devparse.py, then put it anywhere you find convenient. Simply drag the csv you wish to process onto the bat and it will execute.

For more fun, modify the .reg file so it points to your .bat file (be mindful of the "\\"'s and the "\" after .bat). Then run the .reg file. This will put a new command in your context menu called "Process Deviations". Right click the file you want to process and select "Process Deviations" and the program will execute. 
