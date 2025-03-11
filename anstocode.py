
import re
import fileinput

modeline = r'[#;] v' + 'im:'

def main ():
    in_vb = 0
    in_cb = 0
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
        if first == 'CB(':
            in_cb = 1
            print("")
            continue
        if first == 'CB)':
            in_cb = 0
            continue
        if in_cb:
            print(line)
            continue


main()

