
import re
import fileinput

modeline = r'[#;] v' + 'im:'

def main ():
    in_vb = 0
    in_zone = 0
    begins = 'CB('
    ends   = 'CB)'
    preamble = ""
    postamble = ""
    print(preamble, end='\n')
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
        if first == begins:
            in_zone = 1
            print("", end='\n')
            continue
        if first == ends:
            in_zone = 0
            continue
        if in_zone:
            print(line, end='\n')
            continue
    print(postamble, end='\n')

main()

