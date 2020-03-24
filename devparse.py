#!/usr/bin/python3
#
# Name: DevParse
# Version 1.0
# Created by: pvtcompyle
# Desc: Used to parse deviation reports
# Updated: 24-Mar-2020

import sys
import time
import pandas as pd
import re
import os
import glob
import numpy as np
import shutil
import argparse
import ntpath

def getcsv():
    extension = 'csv'
    files = glob.glob('*.{}'.format(extension))
    return(files)

def getDataFrame(file):
    data_frame = pd.read_csv(file, sep=',')
    return(data_frame)

def getEmplList(file, dir):
    data_frame = pd.read_csv(file)
    employees = data_frame['EmployeesInvolved'].unique()
    employeelist = []

    for e in employees:
        empline = e.splitlines()
        for l in empline:
            if len(l)>0:
                employeelist.append(l.upper())
    employeelist.sort()
    employeelist = np.array(employeelist)
    employeelist = np.unique(employeelist)
    return(employeelist)

def seperateemployees(file, employeelist, dir, reportdate):
    data_frame = pd.read_csv(file)
    employeefile = reportdate + '_Employees.xlsx'
    writer = pd.ExcelWriter(employeefile, engine='xlsxwriter')
    dropList = ["Center", "DaysOpen", "Status", "DateClosed", "RootCause", "AssociatedDeviationCAPANumber"]
    for e in employeelist:
        result = data_frame[data_frame['EmployeesInvolved'].str.contains(e,case= False)]
        result = result.drop(dropList, axis=1)
        result.to_excel(writer, sheet_name=e, index=False)
    writer.save()
    
    print('Employees have been seperated into individual sheets in file ', employeefile)

def summary(data_frame,summaryfile,employeelist, employeecount):
    EmployeeSummary = []
    print('\nCounting deviations per employee ...')

    # Get employee deviation counts
    for h in employeelist:
        employeeresult = data_frame[data_frame['EmployeesInvolved'].str.contains(h, case=False)]
        dev_count = len(employeeresult)
        EmployeeSummary.append([h, dev_count])

    print('Counts complete.')
    print('Employees = ', len(employeelist))
    # Write summary to file
    print('\nWriting summary to file ...')
    for h in EmployeeSummary:
        pd.DataFrame(EmployeeSummary).to_csv(summaryfile, sep=',', header=['Employee','Deviations'], index=False)
    EmployeeSummary = getDataFrame(summaryfile)
    print('\nSorting by deviation count and rewriting file ... ')
    EmployeeSummary = EmployeeSummary.sort_values(by=['Deviations'], ascending=False)

    employeecount = len(EmployeeSummary)
    for e in EmployeeSummary:
        pd.DataFrame(EmployeeSummary).to_csv(summaryfile, sep=',', index=False)

def write_to_file(array, outfile):
    try:
        pd.DataFrame(array).to_csv(outfile, index=False, header=None)
    except:
        print('Could not write to ',outfile, ': Access Denied.')
        if not input('Try again? (y/n)') == 'y': return
        write_to_file(array, outfile)

def correctDate():
    value= input('Please enter the correct date (ex. 2020-02-28): ')
    while not re.match( r'(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])', value):
        print(F'Incorrect date format or values out of range!')
        value = input('Please enter correct date (ex. 2020-02-28): ')
    return str(value)

def main():
    ################
    ## Initialize ##
    ################

    # Parse passed arguments
    parser = argparse.ArgumentParser(description='must include a filename to process.')
    parser.add_argument("-p")
    args = parser.parse_args()
    reportFile = args.p
    reportFile= ntpath.basename(reportFile)
    cwd = ntpath.dirname(reportFile)
    print("Reprot to run: ", reportFile)

    reportdate = time.strftime('%Y-%m-%d')
    check=""

    employeelist= []
    if len(reportFile) < 1:
        reportFile = input('Please enter a file name with correct path: ')

    # Create new folder for output files
    path = str(reportdate) + '_' + re.sub('\.csv', '', reportFile)

    if not os.path.exists(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        time.sleep(.300)
        os.mkdir(path)
    
    # Get reportdate 
    while check!="y":
        check=input('Is this the correct report date: ' + str(reportdate) + '? (y/n): ')
        if check!='y':
            reportdate = correctDate()
    summary_file = reportdate + '_Summary.csv'

    #################
    # Begin Program #
    #################

    # Copy and rename report file
    processFile = str(reportdate) +'_' + reportFile
    print(processFile, reportFile, path)

    shutil.copy(reportFile, path)

    # Begin processing files
    os.chdir(path)
    summary_df = getDataFrame(reportFile)
    employeelist = getEmplList(reportFile, 'employees')
    employeecount = len(employeelist)
    summary(summary_df, summary_file, employeelist, employeecount)
    seperateemployees(reportFile, employeelist, 'employees', reportdate)
   
    # End program
    print('Processing complete ...')

main()