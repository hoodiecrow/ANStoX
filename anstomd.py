
import re
import html
import dicttxt
import fileinput

baseURL = "https://github.com/hoodiecrow/ConsTcl"
modeline = r'[#;] v' + 'im:'

cline = ""
csep = ""

b = re.compile('B\{([^{}]+)\}')
e = re.compile('E\{([^{}]+)\}')
k = re.compile('K\{([^{}]+)\}')
i = re.compile('I\{([^{}]+)\}')
f = re.compile('F\{([^{}]+)\}')
r = re.compile('R\{([^{}]+)\}\{([^{}]+)\}')
s = re.compile('S\{([^{}]+)\}\{([^{}]+)\}')
l = re.compile('L\{([^{}]+)\}\{([^{}]+)\}')
w = re.compile('W\{([^{}]+)\}\{([^{}]+)\}')
p = re.compile('P\{([^{}]+)\}\{([^{}]+)\}')

def main ():
    db = dicttxt.makedb()
    in_vb = 0
    in_cb = 0
    in_pr = 0
    in_tt = 0
    in_it = 0
    in_en = 0
    in_dl = 0
    h1 = re.compile('^[Hh]1$')
    h2 = re.compile('^[Hh]2$')
    h3 = re.compile('^[Hh]3$')
    h4 = re.compile('^[Hh]4$')
    h5 = re.compile('^[Hh]5$')
    h6 = re.compile('^[Hh]6$')
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
            print('\n```')
            in_vb = 1
            continue
        if (first == 'VB)'):
            print('```')
            in_vb = 0
            continue
        if (in_vb):
            print(line)
            continue
        if (first == 'PR('):
            in_pr = 1
            continue
        if (first == 'PR)'):
            in_pr = 0
            continue
        if (in_pr):
            try:
                (th, tds) = line.split(';')
            except ValueError:
                print('FOO', line)
            print("\n<table border=1>", end="")
            print(f'<thead><tr><th colspan=2 align=\"left\">{htmlify(th)}</th></tr></thead>', end="")
            for td1, td2 in zip(*[iter(tds.split())]*2):
                td2 = db[td2]
                if (td1 == '->'):
                    print(f'<tr><td><i>Returns:</i></td><td>{htmlify(td2)}</td></tr>', end="")
                else:
                    print(f'<tr><td>{htmlify(td1)}</td><td>{htmlify(td2)}</td></tr>', end="")
            print('</table>')
            continue
        if (h1.match(first)):
            fields[0] = "#"
            str = ' '.join(fields)
            print()
            print(str)
            continue
        if (h2.match(first)):
            fields[0] = "##"
            str = ' '.join(fields)
            print()
            print(str)
            continue
        if (h3.match(first)):
            fields[0] = "###"
            str = ' '.join(fields)
            print()
            print(str)
            continue
        if (h4.match(first)):
            fields[0] = "####"
            str = ' '.join(fields)
            for k, v in {'"!': '!', '"@': '@', '"|': '|'}.items():
                str = str.replace(k, v)
            print()
            print(str)
            continue
        if (h5.match(first)):
            fields[0] = "#####"
            str = ' '.join(fields)
            print()
            print(str)
            continue
        if (h6.match(first)):
            fields[0] = "######"
            str = ' '.join(fields)
            print()
            print(str)
            continue
        if first == 'IX':
            continue
        if first == 'IG':
            print()
            print(f'![#]({second[1:]})')
            continue
        if first == 'IF':
            fields = fields[2:]
            caption = ' '.join(fields)
            print()
            print(f'![#]({second[1:]} "{caption}")')
            caption = ''
            continue
        if first == 'EM':
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print()
            print(f'_{str}_')
            continue
        if first == 'KB':
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print()
            print(f'``{str}``')
            continue
        if first == 'NI':
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print()
            print(str)
            continue
        if first == 'CB(':
            in_cb = 1
            print("\n```")
            continue
        if first == 'CB)':
            in_cb = 0
            print("```")
            continue
        if in_cb:
            print(line)
            continue
        if first == 'TT(':
            in_tt = 1
            continue
        if first == 'TT)':
            in_tt = 0
            continue
        if in_tt:
            continue
        if first == 'IT':
            if not in_it:
                print()
            in_it = 1
            fields[0] = '*'
            str = ' '.join(fields)
            str = render(str)
            print(str)
            continue
        if in_it and first != 'IT':
            in_it = 0
            continue
        if first == 'EN':
            if not in_en:
                print()
            in_en = 1
            fields[0] = '1.'
            str = ' '.join(fields)
            str = render(str)
            print(str)
            continue
        if in_en and first != 'EN':
            in_en = 0
            continue
        if first == 'DL':
            if not in_dl:
                print()
            in_dl = 1
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            label, deftext = re.split(r' LD ', str)
            print(f'1. {label}  \n{deftext}')
            continue
        if in_dl and first != 'DL':
            in_dl = 0
            continue
        if first == 'PT(':
            print("\n\n---\n")
            continue
        if first == 'PT)':
            print("\n\n---\n")
            continue
        if line == '':
            flushp()
        else:
            for field in fields:
                collect(field)
    flushp()
    print('\n')


def collect (v):
    global cline
    global csep
    cline = cline + csep + v
    csep = ' '

def flushp ():
    global cline
    global csep
    if cline != '':
        print(f'\n{render(cline)}')
        cline = ''
        csep = ''

def htmlify (str):
    return html.escape(str, False)

def render (str):
    global b
    global e
    global k
    global i
    global f
    global r
    global s
    global l
    global w
    global p
    for x, y in {'\{': '{', '\}': '}', '==>': '⇒'}.items():
        str = str.replace(x, y)
    str = b.sub(brepl, str, 20)
    str = e.sub(erepl, str, 20)
    str = k.sub(krepl, str, 30)
    str = i.sub(irepl, str, 10)
    str = f.sub(frepl, str, 10)
    str = r.sub(rrepl, str, 20)
    str = s.sub(srepl, str, 20)
    str = l.sub(lrepl, str, 20)
    str = w.sub(wrepl, str, 20)
    str = p.sub(prepl, str, 20)
    return str

def brepl (matchobj):
    return '__' + matchobj.group(1) + '__'

def erepl (matchobj):
    return '_' + matchobj.group(1) + '_'

def krepl (matchobj):
    return '`` ' + matchobj.group(1) + ' ``'

def irepl (matchobj):
    return ''

def frepl (matchobj):
    return r' (' + matchobj.group(1) + ')'

def rrepl (matchobj):
    global baseURL
    return f'[{matchobj.group(1)}]({baseURL}#{matchobj.group(2)})'

def srepl (matchobj):
    global baseURL
    return f'[``{matchobj.group(1)}``]({baseURL}#{matchobj.group(2)})'

def lrepl (matchobj):
    return f'[{matchobj.group(1)}]({matchobj.group(2)})'

def wrepl (matchobj):
    return f'[{matchobj.group(1)}](https://en.wikipedia.org/wiki/{matchobj.group(2)})'

def prepl (matchobj):
    return f'{matchobj.group(1)}<sup>{matchobj.group(2)}</sup>'


main()

