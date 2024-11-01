#!/usr/bin/python3

import argparse
import csv
import os.path
import textwrap
import sys
import string

# get filter on printable characters only
# https://stackoverflow.com/questions/8689795/how-can-i-remove-non-ascii-characters-but-leave-periods-and-spaces-using-python
printable = set(string.printable)

parser = argparse.ArgumentParser(description="Process CSV files and adjust the fields according to specification provided while outputting meta information that could be helpful.\nAuthor: Andy Chien (andy_chien@hotmail.com)")
parser.add_argument('--def-file', type=str, required=True, help='File containing the destination column definition')
parser.add_argument('--def-file-sep', type=str, required=True, help='Separator for the definition file')
parser.add_argument('--data-file', type=str, required=True, help='The data file to be adjusted in accordance to the column specification outlined by --def-file')
parser.add_argument('--data-file-sep', type=str, required=True, help='Separator for the data file')
parser.add_argument('--out-file', type=str, help='The final output of the process')

args = parser.parse_args()

# print(vars(args))

def setSeparator(sep, typ):
    if sep=='t':
        return '\t'
    elif len(sep)==1:
        return sep
    else:
        print("*** Invalid separator supplied for %s file" % typ)
        exit(1)

def_file_sep = setSeparator(args.def_file_sep, "definition")
data_file_sep = setSeparator(args.data_file_sep, "data")

if not(os.path.isfile(args.def_file) and os.path.isfile(args.data_file)):
    print("Files do not exist")
    exit(1)

def getHeader(fpath, sep):
    with open(fpath) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=sep)
        csvheader=next(csvreader)
        for n, item in enumerate(csvheader):
            csvheader[n] = ''.join(filter(lambda x: x in printable, csvheader[n].upper().strip()))
        return csvheader

defheader = getHeader(args.def_file, def_file_sep)
dataheader = getHeader(args.data_file, data_file_sep)

#print(type(defheader))
#print(', '.join(defheader))

def listToHA(lst):
    return {i:1 for i in lst}

defheaderHA=listToHA(defheader)
dataheaderHA=listToHA(dataheader)

#print(type(defheaderHA))

def getMissing(srclst, dstHA):
    missing=[]
    for i in srclst:
        if not(i in dstHA.keys()):
            missing.append(i)
            #print "append %s" % i
    return missing

dataMissing = getMissing(defheader, dataheaderHA)
defMissing = getMissing(dataheader, defheaderHA)

#print dataMissing
#print defMissing

#print(', '.join(defheader))
#print(', '.join(dataheader))

def printWI(string):
    ret = ""
    for s in textwrap.wrap(string,70):
        ret+="    "+s+"\n"
    return ret
    

print("*** data file is missing the following fields (will be populated as blank "")\n%s\n" % printWI(', '.join(dataMissing)))
print("*** definition file is missing the following fields (will be dropped)\n%s\n" % printWI(', '.join(defMissing)))

def isNumber(obj):
    return isInstance(obj,numbers.Number)

map = []

for i in defheader:
    isMissing=False
    for j in dataMissing:
        if i==j:
            map.append("")
            isMissing=True
    if not(isMissing):
        for ctr,j in enumerate(dataheader):
            if i==j:
                map.append(ctr)

# print(map)

if args.out_file is not None:
    with open(args.data_file) as csvsrc, open(args.out_file, 'w', newline='\n') as csvout:
        csvreader = csv.reader(csvsrc, delimiter=data_file_sep)
        csvwriter = csv.writer(csvout, delimiter=data_file_sep)
        csvwriter.writerow(defheader);
        for line,row in enumerate(csvreader):
            if line > 0:
                newrow=[]
                for ctr,i in enumerate(defheader):
                    if map[ctr]=="":
                        newrow.append("")
                    else:
                        newrow.append(row[map[ctr]])
                csvwriter.writerow(newrow)

sys.exit(0)
