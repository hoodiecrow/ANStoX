# see https://www.mgmarlow.com/words/2024-03-23-markdown-awk/

{ gsub(/\r/, ""); }

BEGIN { modeline = "[#;] v" "im:" }

END { print "\n" }

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
$1 == "PR(" { inside_pr_block = 1; next; }
$1 == "PR)" { inside_pr_block = 0; next; }
inside_pr_block {
	if (match($0, /;/)) {
		printf "<table border=1>";
		th = substr($0, 1, RSTART-1);
		printf "<thead><tr><th colspan=2 align=\"left\">%s</th></tr></thead>", html_textify(th);
		$0 = substr($0, RSTART+RLENGTH);
		for (i = 1; i <= NF; i += 2) {
			td1 = ($i == "->" ? "Returns:" : $i);
			td2 = dict[$(i+1)];
			if (td1 == "Returns:")
				printf "<tr><td><i>%s</i></td><td>%s</td></tr>", html_textify(td1), html_textify(td2);
			else
				printf "<tr><td>%s</td><td>%s</td></tr>", html_textify(td1), html_textify(td2);
		}
		print "</table>\n";
	}
	next;
}

# minimalist function that encodes a string as HTML text
function html_textify(str) {
	gsub(/&/, "\\&amp;", str);
	gsub(/</, "\\&lt;", str);
	gsub(/>/, "\\&gt;", str);
	return str;
}


########################## second part ############################
# do simple replacement on entities
#
# Hn to n x #
$1 ~ /^[Hh]1/ { $1 = "#" ; print ; next }
$1 ~ /^[Hh]2/ { $1 = "##" ; print ; next }
$1 ~ /^[Hh]3/ { $1 = "###" ; print ; next }
$1 ~ /^[Hh]4/ {
	# the text for the h4 tag might have "-escaped characters
	gsub(/"!/, "!", $0)
	gsub(/"@/, "@", $0)
	gsub(/"\|/, "|", $0)
       	$1 = "####"
	print
       	next
}
$1 ~ /^[Hh]5/ { $1 = "#####" ; print ; next }
$1 ~ /^[Hh]6/ { $1 = "######" ; print ; next }

# index in LaTeX filter, just ignore here
$1 == "IX" { next }
# IG = Include Graphic
$1 == "IG" { printf("![#](%s)\n", substr($2, 2)) ; next }
# LaTeX filter treats IF differently, placing image in a
# float with a caption
$1 == "IF" { printf("![#](%s)\n", substr($2, 2)) ; next }

# wrap line in _ to render it in italics
$1 == "EM" { $1 = "" ; $2 = "_" $2 ; $NF = $NF "_" ; $0 = "\n" render($0) "\n" ; print ; next }
# wrap line in `` to render it in monospace
$1 == "KB" { $1 = "" ; $2 = "``" $2 ; $NF = $NF "``" ; $0 = "\n" render($0) "\n" ; print ; next }
# in the LaTeX filter, this is "noindent"
$1 == "NI" { $1 = "" ; $0 = "\n" render($0) "\n" ; print ; next }

########################## third part #############################
# deal with blocks
#
# print the CB block
$1 == "CB(" { in_cb_block = 1 ; print "```" ; next }
$1 == "CB)" { in_cb_block = 0 ; print "```" ; next }
in_cb_block { print ; next }

# skip the TT block
$1 == "TT(" { in_tt_block = 1 ; next }
$1 == "TT)" { in_tt_block = 0 ; next }
in_tt_block { next }

# bulleted list...
$1 == "IT" { in_it = 1; $1 = "*" ; $0 = render($0) ; print ; next }
in_it && $1 != "IT" { in_it = 0; next }
# ...and numbered list
$1 == "EN" { in_en = 1; $1 = "1." ; $0 = render($0) ; print ; next }
in_en && $1 != "EN" { in_en = 0; next }

# markdown block
$1 == "MD(" { in_md_block = 1 ; print "" ; next }
$1 == "MD)" { in_md_block = 0 ; flushp() ; next }
in_md_block && /./  { for (i=1; i<=NF; i++) collect($i) }
in_md_block && /^$/ { flushp() }

# in LaTeX filter this is pulled text: an aside
$1 == "PT(" { print "\n\n---\n" ; next }
$1 == "PT)" { print "\n\n---\n" ; next }

# verbatim block
$1 == "VB(" { in_vb_block = 1 ; print "```" ; next }
$1 == "VB)" { in_vb_block = 0 ; print "```"   ; next }
in_vb_block { print ; next }

########################## fourth part #############################
# formatting functions
#
# Concatenate our multi-line string
function collect(v) {
  line = line sep v
  sep = " "
}

# Flush the string, rendering any inline elements
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

    # bold text
    while (match(line, /B{([^{}]+)}/)) {
        sub(/B{([^{}]+)}/, sprintf("__%s__", substr(line, RSTART+2, RLENGTH-3)), line)
    }
    
    # italic text
    while (match(line, /E{([^{}]+)}/)) {
        sub(/E{([^{}]+)}/, sprintf("_%s_", substr(line, RSTART+2, RLENGTH-3)), line)
    }

    # keyboard text
    while (match(line, /K{([^{}]+)}/)) {
        sub(/K{([^{}]+)}/, sprintf("`` %s ``", substr(line, RSTART+2, RLENGTH-3)), line)
    }

    # another way to write an index entry in LaTeX filter
    if (match(line, /I{([^{}]+)}/)) {
        gsub(/I{([^{}]+)}/, "", line)
    }

    # in LaTeX filter, this is footnote
    while (match(line, /F{([^{}]+)}/)) {
        sub(/F{([^{}]+)}/, sprintf(" (%s)", substr(line, RSTART+2, RLENGTH-3)), line)
    }

    # 
    while (match(line, /M{([^{}]+)}/)) {
        sub(/M{([^{}]+)}/, sprintf("__%s__", substr(line, RSTART+2, RLENGTH-3)), line)
    }

    # reference
    while (match(line, /R{([^{}]+)}{([^{}]+)}/)) {
	patsplit(substr(line, RSTART+2, RLENGTH-3), ref, /[^{}]+/)
        sub(/R{([^{}]+)}{([^{}]+)}/, sprintf("[%s](https://github.com/hoodiecrow/ConsTcl#%s)", ref[1], ref[2]), line)
    }

    # reference with keyboard formatting around anchor text
    while (match(line, /S{([^{}]+)}{([^{}]+)}/)) {
	patsplit(substr(line, RSTART+2, RLENGTH-3), ref, /[^{}]+/)
        sub(/S{([^{}]+)}{([^{}]+)}/, sprintf("[``%s``](https://github.com/hoodiecrow/ConsTcl#%s)", ref[1], ref[2]), line)
    }

    # link
    while (match(line, /L{([^{}]+)}{([^{}]+)}/)) {
	patsplit(substr(line, RSTART+2, RLENGTH-3), link, /[^{}]+/)
        sub(/L{([^{}]+)}{([^{}]+)}/, sprintf("[%s](%s)", link[1], link[2]), line)
    }

    # wikipedia link
    while (match(line, /W{([^{}]+)}{([^{}]+)}/)) {
	patsplit(substr(line, RSTART+2, RLENGTH-3), wiki, /[^{}]+/)
        sub(/W{([^{}]+)}{([^{}]+)}/, sprintf("[%s](https://en.wikipedia.org/wiki/%s)", wiki[1], wiki[2]), line)
    }

    # a way to write x to the power of y
    while (match(line, /P{([^{}]+)}{([^{}]+)}/)) {
	patsplit(substr(line, RSTART+2, RLENGTH-3), pow, /[^{}]+/)
        sub(/P{([^{}]+)}{([^{}]+)}/, sprintf("%s<sup>%s</sup>", pow[1], pow[2]), line)
    }

    # replace with arrow character
    if (match(line, /==>/)) { gsub(/==>/, "⇒", line) }

    return line
}

# Vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab:

