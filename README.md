﻿# csv-reorder

## Purpose
csv-reorder is a simple tool that reorders the columns of the csv file based on a reference definition file; regardless of the casing of the field header.

This tool is for you if you need to
1. Reorder CSV of the source data to the database is needed in order to 
keep the SQL INSERT INTO syntax simple by ensuring the CSV source data mirrors 
the database schema.
2. Pair this with applications that does not respect CSV column order (like 
Tableau Prep) in order to to ensure the CSV file has consistent column order 
for other business application.
3. You want to keep your column reordering operations simple. This tool reads 
all fields in as strings. It does not apply any advance (and unpredictable) 
algorithm to determine data type and data length that may inadvertently 
alter your data as part or the reorder operations when compare to other 
approaches; no muss no fuss.

## Installation
There is no user interface to this program, it will have to be executed through PowerShell or bash.

### Windows
Either use as Python script in [src/csv-reorder.py](https://github.com/andychien009/csv-reorder/blob/main/src/csv-reorder.py) or pyinstaller packaged win10 encoded *.exe file in [bin/csv-reorder.exe](https://github.com/andychien009/csv-reorder/blob/main/bin/csv-reorder.exe).

No Python installation is required when using the executable. The win10 packaged executable is tested to be working with Windows 11.

To make things easier, simply put csv-reorder.exe at the folder you wish to execute.

_(Optional)_ For more advanced and frequent execution, it is possible to put the csv-reorder.exe executable in a folder and point the $env:path variable to it so that it can be accessible in every directory in PowerShell.

```PowerShell
New-Item -Path $profile -Type File
notepad.exe "$profile"
```

**$profile**
```PowerShell
$env:path = "<path to your bin dir>;" + $env:path
```

### Linux
If you wish to use this in linux, simply place the python script in your
$HOME\bin directory and give it executable flag by

```bash
chmod 744 ~/bin/csv-reorder.py
```


## General Use Overview
To use the tool first supply the following 4 flags and their respective
arguments to see a preview {--data-file, --data-file-sep, --def-file, 
--def-file-sep}

Once satisfied with the overview of the output, supply the {--out-file} flag 
and and the output file to produce the re-ordered file

## Arguments Input
```
      -h, --help            show this help message and exit
      --def-file DEF_FILE   File containing the destination column definition
      --def-file-sep DEF_FILE_SEP
                            Separator for the definition file
      --data-file DATA_FILE
                            The data file to be adjusted in accordance to the
                            column specification outlined by --def-file
      --data-file-sep DATA_FILE_SEP
                            Separator for the data file
      --out-file OUT_FILE   The final output of the process
```

The following are the files are used for the example

**data.csv**
```
a,b,c
11,12,13
21,22,23
```

One can acquire the database schema that will establish column order easily by doing a SELECT * query and save the result as CSV. The ease of producing the definition file that will establish the column order is exactly as per the design of this tool.

```SQL
SELECT TOP 1 *
FROM TBLNAME;
```

**definition.csv**
```
a,c,d
11,12,13
```

```PowerShell
csv-reorder.exe --def-file definition.csv --def-file-sep ',' \
                --data-file data.csv --data-file-sep ','

*** data file is missing the following fields (will be populated as blank )
    D


*** definition file is missing the following fields (will be dropped)
    B
```

When you do not supply the output file as the final parameter you can get an
overview to the following
1. Columns that will be dropped because they are not in the definition file
2. Columns that will be added as blank because they are not in the data file

Once you are comfortable with the assessment you can complete the run by
issuing the command with the output flag

```PowerShell
csv-reorder.exe --def-file definition.csv --def-file-sep ',' \
                --data-file data.csv --data-file-sep ','

*** data file is missing the following fields (will be populated as blank )
    D


*** definition file is missing the following fields (will be dropped)
    B
```

**out.csv**
```
A,C,D
11,13,
21,23,
```

You can see from the final result that the out.csv file now contains data that
conforms with the definition.csv provided in the same order. It only contains 
data from the data.csv.

Also note the field names have been capitalized. If that is not desired,
simply open the definition.csv and copy the header over.

## Known Issue
This tool outputs header column in capital case. Take the header from
the definition file if you so choose.

This tool does not process fields that are not of printable characters.

## License and Rights
The content of this repo is written and put together by Andy Chien. You can
reach me at andy_chien@hotmail.com.

All content in this repo is under GNU GPL v3. See LICENSE for more information

## Dedication
For my loving family, Jina Julia and Alison.
