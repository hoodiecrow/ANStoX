
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
            print('')
            print(r'\begin{verbatim}')
            in_vb = 1
            continue
        if (first == 'VB)'):
            print(r'\end{verbatim}')
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
            print('')
            print(r"\noindent\begin{tabular}{ |p{1.9cm} p{8cm}| }")
            print(r"\hline")
            print(r"\rowcolor[HTML]{CCCCCC} \multicolumn{2}{|l|}{\bf ", end="")
            print(f"{th}", end="")
            print(r"} \\")
            for td1, td2 in zip(*[iter(tds.split())]*2):
                td2 = db[td2]
                if (td1 == '->'):
                    print(r'\textit{Returns:} & ' + latexify(td2) + ' \\\\')
                else:
                    print(latexify(td1) + ' & ' + latexify(td2) + ' \\\\')
            print(r"\hline")
            print(r"\end{tabular}")
            continue
        if (h1.match(first)):
            fields = fields[1:]
            str = ' '.join(fields)
            elt = r'\part{' + str + '}'
            lbl = r'\label{' + makelabel(str) + '}'
            print('')
            print(elt)
            print(lbl)
            continue
        if (h2.match(first)):
            fields = fields[1:]
            str = ' '.join(fields)
            elt = r'\chapter{' + str + '}'
            lbl = r'\label{' + makelabel(str) + '}'
            print('')
            print(elt)
            print(lbl)
            continue
        if (h3.match(first)):
            lower_case = (fields[0] == 'h3')
            fields = fields[1:]
            str = ' '.join(fields)
            if lower_case:
                idx = r'\index{' + str.lower() + '}'
            else:
                idx = r'\index{' + str + '}'
            elt = r'\section{' + str + '}'
            lbl = r'\label{' + makelabel(str) + '}'
            print('')
            print(elt)
            print(lbl)
            print(idx)
            continue
        if (h4.match(first)):
            lower_case = (fields[0] == 'h4')
            fields = fields[1:]
            str = ' '.join(fields)
            if lower_case:
                idx = r'\index{' + str.lower() + '}'
            else:
                idx = r'\index{' + str + '}'
            for k, v in {'"!': '!', '"@': '@', '"|': '|'}.items():
                str = str.replace(k, v)
            elt = r'\subsection{' + str + '}'
            lbl = r'\label{' + makelabel(str) + '}'
            print('')
            print(elt)
            print(lbl)
            print(idx)
            continue
        if (h5.match(first)):
            lower_case = (fields[0] == 'h5')
            fields = fields[1:]
            str = ' '.join(fields)
            if lower_case:
                idx = r'\index{' + str.lower() + '}'
            else:
                idx = r'\index{' + str + '}'
            elt = r'\subsubsection{' + str + '}'
            lbl = r'\label{' + makelabel(str) + '}'
            print('')
            print(elt)
            print(lbl)
            print(idx)
            continue
        if (h6.match(first)):
            fields = fields[1:]
            str = ' '.join(fields)
            elt = r'\paragraph{' + str + '}'
            lbl = r'\label{' + makelabel(str) + '}'
            print('')
            print(elt)
            print(lbl)
            continue
        if first == 'IX':
            print(r'\index{' + line[3:] + '}')
            continue
        if first == 'IG':
            print('')
            print(r"\includegraphics{" + second[1:] + "}")
            continue
        if first == 'IF':
            fields = fields[2:]
            caption = ' '.join(fields)
            print('')
            print(r"\begin{figure}[h!]", end="")
            print(r"\includegraphics{" + second[1:] + "}", end="")
            print(r"\captionsetup{labelformat=empty}", end="")
            print(r"\caption{" + caption + "}", end="")
            print(r"\label{fig:" + makelabel(caption) + "}", end="")
            print(r"\end{figure}")
            caption = ''
            continue
        if first == 'EM':
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print('')
            print(r'\emph{' + str + '}')
            continue
        if first == 'KB':
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print('')
            print(r'\texttt{' + str + '}')
            continue
        if first == 'NI':
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print('')
            print(r"\noindent " + str)
            continue
        if first == 'CB(':
            in_cb = 1
            print('')
            print(r"\begin{lstlisting}")
            continue
        if first == 'CB)':
            in_cb = 0
            print(r"\end{lstlisting}")
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
                print('')
                print(r"\begin{itemize}")
            in_it = 1
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print(r"\item " + str)
            continue
        if in_it and first != 'IT':
            print(r"\end{itemize}")
            in_it = 0
            continue
        if first == 'EN':
            if not in_en:
                print('')
                print(r"\begin{enumerate}")
            in_en = 1
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            print(r"\item " + str)
            continue
        if in_en and first != 'EN':
            print(r"\end{enumerate}")
            in_en = 0
            continue
        if first == 'DL':
            if not in_dl:
                print('')
                print(r"\begin{description}")
            in_dl = 1
            fields = fields[1:]
            str = ' '.join(fields)
            str = render(str)
            label, deftext = re.split(r' LD ', str)
            print(rf'\item[{label}] {deftext}')
            continue
        if in_dl and first != 'DL':
            print(r"\end{description}")
            in_dl = 0
            continue
        if first == 'PT(':
            print("")
            print(r"\begin{pulledtext}")
            continue
        if first == 'PT)':
            print(r"\end{pulledtext}")
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
    for x, y in {r'\{': 'LBRACE', r'\}': 'RBRACE'}.items():
        str = str.replace(x, y)
    str = re.sub(r'\\', r'\\textbackslash ', str)
    for x, y in {'LBRACE': r'\{', 'RBRACE': r'\}'}.items():
        str = str.replace(x, y)
    str = b.sub(brepl, str, 20)
    str = e.sub(erepl, str, 20)
    str = k.sub(krepl, str, 30)
    str = i.sub(irepl, str, 10)
    str = f.sub(frepl, str, 10)
    str = re.sub('\.\.\.', r'\\ldots ', str)
    str = re.sub('(La)TeX', r'\\LaTeX ', str)
    str = r.sub(rrepl, str, 20)
    str = s.sub(srepl, str, 20)
    str = l.sub(lrepl, str, 20)
    str = w.sub(wrepl, str, 20)
    str = re.sub('\$', r'\$', str)
    str = p.sub(prepl, str, 20)
    str = re.sub('===>', r'$\\Longrightarrow$', str)
    str = re.sub('==>', r'$\\Rightarrow$', str)
    str = re.sub('#', r'\#', str)
    str = re.sub('&', r'\&', str)
    str = re.sub('_', r'\_', str)
    str = re.sub('%', r'\%', str)
    return str

def latexify (s):
    s = re.sub(r'\$', r'\$', s)
    s = re.sub(r'#',  r'\#', s)
    s = re.sub(r'&',  r'\&', s)
    s = re.sub(r'_',  r'\_', s)
    s = re.sub(r'%',  r'\%', s)
    return s

def makelabel (s):
    global labels
    s = re.sub("[][\"!'#§%&()*+,-./:;<=>?@/^_{|}~]", '', s)
    s = re.sub(' ', '-', s)
    s = s.lower()
    c = 0
    lbl = s
    while lbl in labels:
        c = c + 1
        lbl = s + str(c)
    labels[lbl] = 1
    return lbl

def brepl (matchobj):
    return r'\textbf{' + matchobj.group(1) + '}'

def erepl (matchobj):
    return r'\emph{' + matchobj.group(1) + '}'

def krepl (matchobj):
    return r'\texttt{' + matchobj.group(1) + '}'

def irepl (matchobj):
    return r'\index{' + matchobj.group(1) + '}'

def frepl (matchobj):
    return r'\footnote{' + matchobj.group(1) + '}'

def rrepl (matchobj):
    return matchobj.group(1) + r' (see page \pageref{' + matchobj.group(2) + '})'

def srepl (matchobj):
    return r'\texttt{' + matchobj.group(1) + r'} (see page \pageref{' + matchobj.group(2) + '})'

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

