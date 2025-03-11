
import re
import fileinput

baseURL = "https://github.com/hoodiecrow/ConsTcl"
useurl = 0
modeline = r'[#;] v' + 'im:'

labels = {}
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
    with open('dict.txt', 'r') as f:
        dbtext = f.read()
    db = {}
    for line in dbtext.splitlines():
        (key, val) = re.split(r'\s+->\s+', line)
        db[key] = val
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
            print('\\begin{verbatim}')
            in_vb = 1
            continue
        if (first == 'VB)'):
            print('\\end{verbatim}')
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
            print("\\noindent\\begin{tabular}{ |p{1.9cm} p{8cm}| }\n\\hline")
            print("\\rowcolor[HTML]{CCCCCC} \\multicolumn{2}{|l|}{\\bf ", end="")
            print(f"{th}", end="")
            print("} \\\\")
            for td1, td2 in zip(*[iter(tds.split())]*2):
                td2 = db[td2]
                if (td1 == '->'):
                    print('{\\textit{Returns:}} & {' + latexify(td2) + '} \\\\')
                else:
                    print('{' + latexify(td1) + '} & {' + latexify(td2) + '} \\\\')
            print("\\hline\n\\end{tabular}")
            continue
        if (h1.match(first)):
            fields = fields[1:]
            str = ' '.join(fields)
            elt = '\\part{' + str + '}'
            lbl = '\\label{' + makelabel(str) + '}'
            elt = render(elt)
            print(elt)
            print(lbl)
            continue
        if (h2.match(first)):
            fields = fields[1:]
            str = ' '.join(fields)
            elt = '\\chapter{' + str + '}'
            lbl = '\\label{' + makelabel(str) + '}'
            elt = render(elt)
            print(elt)
            print(lbl)
            continue
        if (h3.match(first)):
            fields = fields[1:]
            str = ' '.join(fields)
            elt = '\\section{' + str + '}'
            lbl = '\\label{' + makelabel(str) + '}'
            idx = '\\index{' + str + '}'
            elt = render(elt)
            print(elt)
            print(lbl)
            print(idx)
            continue
        if (h4.match(first)):
            lower_case = (fields[0] == 'h4')
            fields = fields[1:]
            str = ' '.join(fields)
            if lower_case:
                idx = '\\index{' + str.lower() + '}'
            else:
                idx = '\\index{' + str + '}'
            for k, v in {'"!': '!', '"@': '@', '"|': '|'}.items():
                str = str.replace(k, v)
            elt = '\\subsection{' + str + '}'
            lbl = '\\label{' + makelabel(str) + '}'
            elt = render(elt)
            print(elt)
            print(lbl)
            print(idx)
            continue
        if (h5.match(first)):
            lower_case = (fields[0] == 'h5')
            fields = fields[1:]
            str = ' '.join(fields)
            if lower_case:
                idx = '\\index{' + str.lower() + '}'
            else:
                idx = '\\index{' + str + '}'
            elt = '\\subsubsection{' + str + '}'
            lbl = '\\label{' + makelabel(str) + '}'
            elt = render(elt)
            print(elt)
            print(lbl)
            print(idx)
            continue
        if (h6.match(first)):
            fields = fields[1:]
            str = ' '.join(fields)
            elt = '\\paragraph{' + str + '}'
            lbl = '\\label{' + makelabel(str) + '}'
            elt = render(elt)
            print(elt)
            print(lbl)
            continue
        if first == 'IX':
            print('\\index{' + line[3:] + '}')
            continue
        if first == 'IG':
            print("\\includegraphics{" + second[1:] + "}")
            continue
        if first == 'IF':
            fields = fields[2:]
            caption = ' '.join(fields)
            print("\\begin{figure}[h!]", end="")
            print("\\includegraphics{" + second[1:] + "}", end="")
            print("\\captionsetup{labelformat=empty}", end="")
            print("\\caption{" + caption + "}", end="")
            print("\\label{fig:" + makelabel(caption) + "}", end="")
            print("\\end{figure}")
            caption = ''
            continue
        if first == 'EM':
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print('\\emph{' + str + '}')
            continue
        if first == 'KB':
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print('\\texttt{' + str + '}')
            continue
        if first == 'NI':
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print("\\noindent " + str)
            continue
        if first == 'CB(':
            in_cb = 1
            print("\\begin{lstlisting}")
            continue
        if first == 'CB)':
            in_cb = 0
            print("\\end{lstlisting}")
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
                print("\\begin{itemize}")
            in_it = 1
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print("\\item " + str)
            continue
        if in_it and first != 'IT':
            print("\\end{itemize}")
            in_it = 0
            continue
        if first == 'EN':
            if not in_it:
                print("\\begin{enumerate}")
            in_en = 1
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print("\\item " + str)
            continue
        if in_en and first != 'EN':
            print("\\end{enumerate}")
            in_en = 0
            continue
        if first == 'DL':
            if not in_dl:
                print("\\begin{description}")
            in_dl = 1
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            label, deftext = re.split(r' LD ', str)
            print(f'\\item[{label}] {deftext}')
            continue
        if in_dl and first != 'DL':
            print("\\end{description}")
            in_dl = 0
            continue
        if first == 'PT(':
            print("\n\\begin{pulledtext}")
            continue
        if first == 'PT)':
            print("\\end{pulledtext}\n")
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
        print(f'\n{render(cline)}\n')
        cline = ''
        csep = ''

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
    for x, y in {'\{': 'LBRACE', '\}': 'RBRACE'}.items():
        str = str.replace(x, y)
    str = b.sub(brepl, str, 9)
    str = e.sub(erepl, str, 9)
    str = k.sub(krepl, str, 12)
    str = i.sub(irepl, str, 6)
    str = f.sub(frepl, str, 6)
    str = re.sub('\.\.\.', '\\ldots ', str)
    str = re.sub('(La)TeX', '\\LaTeX ', str)
    str = r.sub(rrepl, str, 9)
    str = s.sub(srepl, str, 9)
    str = l.sub(lrepl, str, 9)
    str = w.sub(wrepl, str, 9)
    str = re.sub('\$', '\\$', str)
    str = p.sub(prepl, str, 9)
    str = re.sub('===>', '$\Longrightarrow\$', str)
    str = re.sub('==>', '$\Rightarrow\$', str)
    str = re.sub('#', '\\#', str)
    str = re.sub('&', '\\&', str)
    str = re.sub('_', '\\_', str)
    str = re.sub('%', '\\%', str)
    return str

def latexify (s):
    s = re.sub(r'\$', '\\$', s)
    s = re.sub(r'#',  '\\#', s)
    s = re.sub(r'&',  '\\&', s)
    s = re.sub(r'_',  '\\_', s)
    s = re.sub(r'%',  '\\%', s)
    return s

def makelabel (str):
    global labels
    str = re.sub('[[:punct:]]', '', str)
    str = re.sub(' ', '-', str)
    str = str.lower()
    c = 0
    lbl = str
    while lbl in labels:
        ++c
        lbl = str + c
    labels[lbl] = 1
    return str

def brepl (matchobj):
    return '\\textbf{' + matchobj.group(1) + '}'

def erepl (matchobj):
    return '\\emph{' + matchobj.group(1) + '}'

def krepl (matchobj):
    return '\\texttt{' + matchobj.group(1) + '}'

def irepl (matchobj):
    return '\\index{' + matchobj.group(1) + '}'

def frepl (matchobj):
    return '\\footnote{' + matchobj.group(1) + '}'

def rrepl (matchobj):
    return matchobj.group(1) + ' (see page \\pageref{' + matchobj.group(2) + '})'

def srepl (matchobj):
    return '\\texttt{' + matchobj.group(1) + '} (see page \\pageref{' + matchobj.group(2) + '})'

def lrepl (matchobj):
    if useurl:
        fmt = 'url'
    else:
        fmt = 'texttt'
    return matchobj.group(1) + '\\footnote{See \\' + fmt + '{' + matchobj.group(2) + '}}'

def wrepl (matchobj):
    if useurl:
        fmt = 'url'
    else:
        fmt = 'texttt'
    return matchobj.group(1) + '\\footnote{See \\' + fmt + '{https://en.wikipedia.org/wiki/' + matchobj.group(2) + '}}'

def prepl (matchobj):
    return '${' + matchobj.group(1) + '}^{' + matchobj.group(2) + '}$'


main()

