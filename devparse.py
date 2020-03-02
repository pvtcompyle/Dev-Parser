#!/usr/bin/python3
#
# Name: vparse
# Version 3.0
# Created by: Thunder Sargent
# Desc: Used to parse and analyze Nessus vulnerability scans
# Updated: 13-Dec-2019

import sys
from colorama import Style, Fore, Back, init
import time
import pandas as pd
import re
import os
import glob
import numpy as np
import shutil

def getcsv():
    extension = 'csv'
    files = glob.glob('*.{}'.format(extension))
    return(files)

def getDataFrame(file):
    data_frame = pd.read_csv(file, sep=',', encoding = 'ISO-8859-1')
    return(data_frame)

def getEmplList(file, dir):
    data_frame = pd.read_csv(file, encoding = 'ISO-8859-1')
    employees = data_frame['EmployeesInvolved'].unique()
    employeelist = []

    for e in employees:
        empline = e.splitlines()
        for l in empline:
            employeelist.append(l.upper())
    employeelist.sort()
    employeelist = np.array(employeelist)
    employeelist = np.unique(employeelist)
    return(employeelist)

def seperateemployees(file, employeelist, dir, reportdate):
    data_frame = pd.read_csv(file, encoding = 'ISO-8859-1')
    
    employeecount = len(employeelist)
    for e in employeelist:
        result = data_frame[data_frame['EmployeesInvolved'].str.contains(e,case= False)]
        employeefile = e + ' ' + reportdate + '.csv'
        employeefile = os.path.join(dir, employeefile)
        result.to_csv(employeefile, sep=',', index=False)
    print(Style.RESET_ALL)
    print(Fore.GREEN + 'Employees have been seperated into individual files.' + Fore.RESET)

def summary(data_frame,summaryfile,employeelist, employeecount):
    EmployeeSummary = []
    print(Fore.BLUE + '\nCounting deviations per employee ...' + Fore.RESET)

    # Get employee deviation counts
    for h in employeelist:
        employeeresult = data_frame[data_frame['EmployeesInvolved'].str.contains(h, case=False)]
        dev_count = len(employeeresult)
        EmployeeSummary.append([h, dev_count])

    print(Fore.GREEN + 'Counts complete.' + Fore.RESET)
    
    # Write summary to file
    print(Fore.BLUE + '\nWriting summary to file ...' + Fore.RESET)
    for h in EmployeeSummary:
        pd.DataFrame(EmployeeSummary).to_csv(summaryfile, sep=',', header=['Employee','Deviations'], index=False)
    EmployeeSummary = getDataFrame(summaryfile)
    print(Fore.BLUE + '\nSorting by deviation count and rewriting file ... ' + Fore.RESET)
    EmployeeSummary = EmployeeSummary.sort_values(by=['Deviations'], ascending=False)

    employeecount = len(EmployeeSummary)
    for e in EmployeeSummary:
        pd.DataFrame(EmployeeSummary).to_csv(summaryfile, sep=',', index=False)

def write_to_file(array, outfile):
    try:
        pd.DataFrame(array).to_csv(outfile, index=False, header=None)
    except:
        print(Fore.RED + 'Could not write to ',outfile, ': Access Denied.' + Style.RESET_ALL)
        if not input('Try again? (y/n)') == 'y': return
        write_to_file(array, outfile)

def correctDate():
    value= input('Please enter the correct date (ex. 2020-02-28): ')
    while not re.match( r'(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])', value):
        print(Fore.RED + 'Incorrect date format or values out of range!' + Style.RESET_ALL)
        value = input('Please enter correct date (ex. 2020-02-28): ')
    return str(value)

def main():
    ################
    ## Initialize ##
    ################
    reportdate = time.strftime('%Y-%m-%d')
    check=""
    cwd = os.getcwd()
    employeelist= []

    # Create new folder for output files
    path = "results"
    employee_path = 'results/employees'

    if not os.path.exists(path):
        os.mkdir(path)
        os.mkdir(employee_path)
    else:
        shutil.rmtree(path)
        time.sleep(.300)
        os.mkdir(path)
        os.mkdir(employee_path)
    
    # Get reportdate 
    while check!="y":
        check=input('Is this the correct report date: ' + Fore.BLUE + str(reportdate) + Style.RESET_ALL + '? (y/n): ')
        if check!='y':
            reportdate = correctDate()
    summary_file = reportdate + '_Summary.csv'

    #################
    # Begin Program #
    #################
    
    # List csv in CWD
    files = getcsv()
    print(Fore.BLUE + '\nList of csv files in CWD' + Fore.RESET)
    for f in files:
        print('\t',f)

    # Show new file names and prepare to rename
    print(Fore.BLUE + '\nRename these files as:' + Fore.RESET)
    
    for f in files:
        print('\t',reportdate+'_'+f)
    ans = input('Continue? (y/n): ')
    if (ans != 'y') and (ans != 'Y'):
        print('Rename aborted ...')
    else:
        start_time = time.time()
        print('\nProcessing ...')
        # Copy files to results dir
        for f in files:
            shutil.copy (f, path)
        # Rename files in results dir
        os.chdir(path)
        for f in files:
            nf = reportdate+'_'+f
            print('Renaming ' + Fore.BLUE + f + Fore.RESET + ' to '+ Fore.CYAN + nf + Fore.RESET)
            try:
                os.rename(f, nf)
            except:
                os.remove(nf)
                os.rename(f, nf)

    print(Fore.BLUE + '\nVerifying rename ...' + Fore.RESET)

    files = getcsv()
    for f in files:
        #summary_file = 'Summary_'+f
        summary_df = getDataFrame(f)
        employeelist = getEmplList(f, 'employees')
        employeecount = len(employeelist)
        summary(summary_df, summary_file, employeelist, employeecount)
        seperateemployees(f, employeelist, 'employees', reportdate)
   
    # Return to starting Dir
    os.chdir(cwd)

    # End program
    print(Fore.GREEN + '\nProcessing complete ...' + Fore.RESET)

main()