
import re
import html
import fileinput

modeline = r'[#;] v' + 'im:'

def main ():
    in_vb = 0
    in_tt = 0
    print('package require tcltest\nsource constcl.tcl\n')
    for line in fileinput.input():
        line = line.rstrip()
        if (re.match(modeline, line)):
            continue
        if (line == ''):
            fields = []
            first = ''
            second = ''
        else:
            fields = line.split()
            first = fields[0]
            if (len(fields) > 1):
                second = fields[1]
            else:
                second = ''
        if (first == 'VB('):
            in_vb = 1
            continue
        if (first == 'VB)'):
            in_vb = 0
            continue
        if (in_vb):
            continue
        if first == 'TT(':
            in_tt = 1
            print("")
            continue
        if first == 'TT)':
            in_tt = 0
            continue
        if in_tt:
            print(line)
            continue
    print('\n::tcltest::cleanupTests')

main()

