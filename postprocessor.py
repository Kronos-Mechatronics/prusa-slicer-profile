#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Postprocessor to run Slicer generated GCode on Kronos 5X machines
"""

import sys
import os
import re

TOOLID = 1
BEDID  = 33

if len(sys.argv) < 2:
    print("Usage: postprocessor.py gcodefile [outfile]")
else:
    infile = sys.argv[1]
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    else:
        outfile = infile

    # open gcode file and read entire file into buffer. The original file must be overwritten (in-place)
    in_file = None
    with open(infile, "r") as f:
        in_file = f.readlines()

    print("parsing gcode file " + infile + " into " + outfile)

    out_file = open(outfile, "w")
    for line in in_file:

        # replace "G92 E0" with "HOME_E"
        if(re.search('^G92.*E0', line)):
            line = "HOME_E" + line[-1]

        # replace "E" with "QE="
        if(re.search('^G.*E\-?\d*.?\d*', line)):
            tmp = re.split('(E\-?\d*\.?\d*)', line)
            line = "G90 " + tmp[0] + "G91 " + tmp[1].replace("E", "QE=") + " G90 " + tmp[2]

        # replace comments ; -> ()
        if line.find(";") > -1:
            tmp = line.split(";", 1)
            line = tmp[0] + "(" + tmp[1][:-1] + ")" + tmp[1][-1] # tmp[1][-1] only contains the linebreak character

        # swallow M106/M107 (fan control)
        if line.find("M106") > -1 or line.find("M107") > -1:
            line = "( " + line[:-1] + " -- command not supported, disabled)" + line[-1]

        # swallow G21 (set units to mm)
        if line.find("G21") > -1:
            line = "( " + line[:-1] + " -- command not supported, disabled)" + line[-1]

        # temperature controls (M109, M190, M104, M140)
        # M140 set bed temp nonblocking
        if(re.search('^M140', line)):
            tmp = re.split('(M140\s*)S(\d*\.?\d*)', line)
            line = "SET_TEMPERATURE[" + str(BEDID) + "," + tmp[2] + ",0]" + tmp[3]
        # M190 set bed temp blocking
        if(re.search('^M190', line)):
            tmp = re.split('(M190\s*)S(\d*\.?\d*)', line)
            line = "SET_TEMPERATURE[" + str(BEDID) + "," + tmp[2] + ",1]" + tmp[3]
        # M104 set hotend temp nonblocking
        if(re.search('^M104', line)):
            tmp = re.split('(M104\s*)S(\d*\.?\d*)', line)
            line = "SET_TEMPERATURE[" + str(TOOLID) + "," + tmp[2] +  ",0]" + tmp[3]
        # M109 set hotend temp blocking
        if(re.search('^M109', line)):
            tmp = re.split('(M109\s*)S(\d*\.?\d*)', line)
            line = "SET_TEMPERATURE[" + str(TOOLID) + "," + tmp[2] + ",1]" + tmp[3]

        # toolchange
        if(re.search('^T0', line)):
            line = "TOOLID[" + str(TOOLID) + "] (Change to FFF)" + line[-1]
        if(re.search('^T1', line)):
            line = "TOOLID[3] (Change to PiezoJet 1)" + line[-1]

        # SMD components (M361 PartID)
        if(re.search('^M361', line)):
            tmp = re.split('(M361\sP)(\d)', line)
            id = tmp[2]
            linebreak = line[-1]
            line = "PICK_COMPONENT[" + str(id) + ", " + str(partshandler.getPartHeight(id)) + "]" + linebreak
            destination = partshandler.getPartDestination(id)
            line += "ALIGN_COMPONENT[" +  str(destination[3]) + "]" + linebreak
            line += "PLACE_COMPONENT[" +  str(destination[0]) + ", " + str(destination[1]) + ", "  + str(destination[2]) + ", 0, 0,]" + linebreak

        out_file.write(line)

