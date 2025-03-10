# see https://www.mgmarlow.com/words/2024-03-23-markdown-awk/

{ gsub(/\r/, ""); }

BEGIN {
	baseURL = "https://github.com/hoodiecrow/ConsTcl"
	modeline = "[#;] v" "im:"
	print "<html>"
	print "<head>"
	print "<title>A HTML document</title>"
	#print "<link rel=\"stylesheet\" href=\"https://cdn.simplecss.org/simple.min.css\">"
	print "</head>"
	print "<body>"
}

END {
	flushp()
	print "</body>\n</html>\n"
}

# skip any modeline
$0 ~ modeline { next; }

######################## first part ###########################
# translate the PR tags to html tables
# 
# load the key/values pairs from dict.txt
# NOTE: NR is equal to FNR only while processing the first file
NR == FNR {
	if (match($0, /[[:space:]]*->[[:space:]]*/))
		dict[substr($0, 1, RSTART-1)] = substr($0, RSTART+RLENGTH);
	next;
}

# expand the PR blocks as HTML tables in the remainder file(s)
$1 == "PR(" { insideprblock = 1; next; }
$1 == "PR)" { insideprblock = 0; next; }
insideprblock {
	if (match($0, /;/)) {
		printf "<table border=1>";
		th = substr($0, 1, RSTART-1);
		printf "<thead><tr><th colspan=2 align=\"left\">%s</th></tr></thead>", htmlify(th);
		$0 = substr($0, RSTART+RLENGTH);
		for (i = 1; i <= NF; i += 2) {
			td1 = ($i == "->" ? "Returns:" : $i);
			td2 = dict[$(i+1)];
			if (td1 == "Returns:")
				printf "<tr><td><i>%s</i></td><td>%s</td></tr>", htmlify(td1), htmlify(td2);
			else
				printf "<tr><td>%s</td><td>%s</td></tr>", htmlify(td1), htmlify(td2);
		}
		print "</table>\n";
	}
	next;
}

# minimalist function that encodes a string as HTML text
function htmlify(str) {
	gsub(/&/, "\\&amp;", str);
	gsub(/</, "\\&lt;", str);
	gsub(/>/, "\\&gt;", str);
	return str;
}

# verbatim block
$1 == "VB(" { invbblock = 1 ; print "<pre>" ; next }
$1 == "VB)" { invbblock = 0 ; print "</pre>"; next }
invbblock { $0 = htmlify($0) ; print ; next }

########################## second part ############################
# do simple replacement on entities
#
# Hn to Hn
$1 ~ /^[Hh]1/ { printf("<h1>%s</h1>\n", substr($0, 4)) ; next }
$1 ~ /^[Hh]2/ { printf("<h2>%s</h2>\n", substr($0, 4)) ; next }
$1 ~ /^[Hh]3/ { printf("<h3>%s</h3>\n", substr($0, 4)) ; next }
$1 ~ /^[Hh]4/ {
	# the text for the h4 tag might have "-escaped characters
	gsub(/"!/, "!", $0)
	gsub(/"@/, "@", $0)
	gsub(/"\|/, "|", $0)
	printf("<h4>%s</h4>\n", substr($0, 4))
       	next
}
$1 ~ /^[Hh]5/ { printf("<h5>%s</h5>\n", substr($0, 4)) ; next }
$1 ~ /^[Hh]6/ { printf("<h6>%s</h6>\n", substr($0, 4)) ; next }

$1 == "IX" { next }
$1 == "IG" { printf("<img src=\"%s\">\n", substr($2, 2)) ; next }
$1 == "IF" { next }
$1 == "EM" {
    for (i=2; i<=NF; i++) collect($i)
    line = render(line)
    line = sprintf("<i>%s</i>", line)
    print "\n" line "\n"
    line = sep = ""
    next
}
$1 == "KB" {
    for (i=2; i<=NF; i++) collect($i)
    line = render(line)
    line = sprintf("<kbd>%s</kbd>", line)
    print "\n" line "\n"
    line = sep = ""
    next
}
$1 == "NI" { next }

########################## third part #############################
# deal with blocks
#
# print the CB block
$1 == "CB(" { incbblock = 1 ; print "<pre><code>" ; next }
$1 == "CB)" { incbblock = 0 ; print "</code></pre>" ; next }

incbblock { $0 = htmlify($0) ; print ; next }

# skip the TT block
$1 == "TT(" { inttblock = 1 ; next }
$1 == "TT)" { inttblock = 0 ; next }
inttblock { next }


# bulleted list...
$1 == "IT" { if (!init) print "<ul>";init = 1; print "<li> " render(substr($0, 3));next }
init && $1 != "IT" { print "</ul>"; init = 0; next }
# ...and numbered list
$1 == "EN" { if (!inen) print "<ol>";inen = 1; print "<li> " render(substr($0, 3));next }
inen && $1 != "EN" { print "</ol>"; inen = 0; next }
# definition list
$1 == "DL" { if (!indl) print "<dl>";indl = 1; $1 = "" ; $0 = render($0) ; split($0, deflis, / LD /) ; printf "<dt>%s</dt><dd>%s\n</dd>", deflis[1], deflis[2] }
indl && $1 != "DL" { print "</dl>"; indl = 0; next }

# in LaTeX filter this is pulled text: an aside
$1 == "PT(" { print "\n<aside>" ; next }
$1 == "PT)" { print "\n</aside>" ; next }


# text block
$1 == "MD(" { inmdblock = 1 ; print "" ; next }
$1 == "MD)" { inmdblock = 0 ; flushp() ; next }
/./  { for (i=1; i<=NF; i++) collect($i) }
/^$/ { flushp() ; print "<p>"}

########################## fourth part #############################
# formatting functions
#
# Concatenate our multi-line string
function collect(v) {
  line = line sep v
  sep = " "
}

# Flush the string, rendering any inline LaTeX elements
function flushp() {
  if (line) {
    print "\n" render(line) "\n"
    line = sep = ""
  }
}

function render(line) {
    # in LaTeX filter, braces need to be escaped, not so here
    if (match(line, /\\{/)) { gsub(/\\{/, "{", line) }
    if (match(line, /\\}/)) { gsub(/\\}/, "}", line) }

    line = htmlify(line)

    # bold text
    while (match(line, /B{([^{}]+)}/)) {
        sub(/B{([^{}]+)}/, sprintf("<b>%s</b>", substr(line, RSTART+2, RLENGTH-3)), line)
    }
    
    # italic text
    while (match(line, /E{([^{}]+)}/)) {
        sub(/E{([^{}]+)}/, sprintf("<em>%s</em>", substr(line, RSTART+2, RLENGTH-3)), line)
    }

    # keyboard text
    while (match(line, /K{([^{}]+)}/)) {
        sub(/K{([^{}]+)}/, sprintf("<kbd>%s</kbd>", substr(line, RSTART+2, RLENGTH-3)), line)
    }

    # a way to write an index entry
    while (match(line, /I{([^{}]+)}/)) {
        sub(/I{([^{}]+)}/, "", line)
    }

    # footnote
    while (match(line, /F{([^{}]+)}/)) {
        sub(/F{([^{}]+)}/, sprintf(" (%s)", substr(line, RSTART+2, RLENGTH-3)), line)
    }

    # marginpar
    while (match(line, /M{([^{}]+)}/)) {
        sub(/M{([^{}]+)}/, "", line)
    }

    # reference
    while (match(line, /R{([^{}]+)}{([^{}]+)}/)) {
	#patsplit(substr(line, RSTART+2, RLENGTH-3), ref, /[^{}]+/)
        sub(/R{([^{}]+)}{([^{}]+)}/, sprintf("<a href=\"%s#%s\">%s</a>", baseURL, ref[2], ref[1]), line)
    }

    # reference with keyboard formatting around anchor text
    while (match(line, /S{([^{}]+)}{([^{}]+)}/)) {
	#patsplit(substr(line, RSTART+2, RLENGTH-3), ref, /[^{}]+/)
        sub(/S{([^{}]+)}{([^{}]+)}/, sprintf("<a href=\"%s#%s\"><kbd>%s</kbd></a>", baseURL, ref[2], ref[1]), line)
    }

    # link
    while (match(line, /L{([^{}]+)}{([^{}]+)}/)) {
	#patsplit(substr(line, RSTART+2, RLENGTH-3), link, /[^{}]+/)
        sub(/L{([^{}]+)}{([^{}]+)}/, sprintf("<a href=\"%s\">%s</a>", link[2], link[1]), line)
    }

    # wikipedia link
    while (match(line, /W{([^{}]+)}{([^{}]+)}/)) {
	#patsplit(substr(line, RSTART+2, RLENGTH-3), wiki, /[^{}]+/)
        sub(/W{([^{}]+)}{([^{}]+)}/, sprintf("<a href=\"https://en.wikipedia.org/wiki/%s\">%s</a>", wiki[2], wiki[1]), line)
    }

    # a way to write x to the power of y
    while (match(line, /P{([^{}]+)}{([^{}]+)}/)) {
	#patsplit(substr(line, RSTART+2, RLENGTH-3), pow, /[^{}]+/)
        sub(/P{([^{}]+)}{([^{}]+)}/, sprintf("%s<sup>%s</sup>", pow[1], pow[2]), line)
    }

    return line
}

# Vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab:

