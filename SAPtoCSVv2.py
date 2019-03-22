#!/usr/bin/env python
import csv
import sys
from io import StringIO
from pathlib import Path

inputfile = sys.argv[1] # get filename from passed argument
outputfile = Path(inputfile).stem + '.csv' # set output filename to same name as source but with csv extension

with open(inputfile, 'r') as infile, open(outputfile, 'w', newline='') as outfile:
    isData = False # assume start of the file is not yet table data
    isHeader = False # assume start of file is not table header
    isFirstHeader = False # assume start of file is not the table header of the first page
    for line in infile:
        csv_input = csv.reader(StringIO(line[1:-2]), delimiter='|', skipinitialspace=True) # remove the first character and the last two characters from the line.
        csv_output = csv.writer(outfile)
        if isData: # when line contains data
            if isHeader: # when line contains header
                if line[0] == '|': # find the header
                    isHeader = False # and unset the header check
            elif isFirstHeader: # when line is the header for the first page
                if line[0] == '|': # find the header
                    csvrow = next(csv_input)
                    headerrow = csvrow # save header row for future comparison
                    csvrow = [element.strip() for element in csvrow] # remove trailing spaces from line
                    csv_output.writerow(csvrow) # write header to file
                    isFirstHeader = False # and unset the first page header check
            else: # when line contains row data
                if line[0] == '|': # find the row
                    csvrow = next(csv_input)
                    if csvrow != headerrow: # skip row if row equals to header row
                        for index, element in enumerate(csvrow): # remove _ from beginning of string
                            if element:
                                if element[0] == '_':
                                    csvrow[index] = element[1:]
                        csvrow = [element.strip() for element in csvrow] # remove trailing spaces from line
                        csv_output.writerow(csvrow) # write row to file
                elif ord(line[0]) == 10: # when the beginning of line is the form feed character, it means next page header is coming up
                    isHeader = True # therefore, set the header check to true
        else: # this code runs at the beginning of the file, while isData is false
            if ord(line[0]) == 10: # find the first line where the form feed character shows
                isData = True # then set that the data begins here
                isFirstHeader = True # and the first page header is coming up


# In[ ]:




