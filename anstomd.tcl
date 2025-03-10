
set baseURL "https://github.com/hoodiecrow/ConsTcl"
append modeline "[#;] v" "im:"

set dbtxt [readFile dict.txt]
foreach dbline [split $dbtxt \n] {
    regexp {(\w+)\s*->\s*(.+)} -> key val
    dict set db $key $val
}

foreach file $argv {
    set in_vb 0
    set in_cb 0
    foreachLine line $file {
        set line [regsub {\r} $line {}]
        set fields [split $line]
        set first [lindex $fields 0]
        set second [lindex $fields 1]
        if {$first eq "VB("} {
            set in_vb 1
            continue
        }
        if {$first eq "VB)"} {
            set in_vb 0
            continue
        }
        if {$in_vb} {
            continue
        }
        if {$first eq "PR("} {
            set in_pr 1
            continue
        }
        if {$first eq "PR)"} {
            set in_pr 0
            continue
        }
        if {$in_pr} {
            regexp {([^;]+);(.*)} -> th tds
            puts -nonewline [format "<table border=1>"]
            puts -nonewline [format "<thead><tr><th colspan=2 align=\"left\">%s</th></tr></thead>" [htmlify $th]]
            foreach {td1 td2} [list $tds] {
                if {$td1 eq "->"} {
                    set td1 Returns:
                } else {
                    set td2 [dict get $db $td1]
                }
                if {$td1 eq "Returns:"} {
                    puts -nonewline [format "<tr><td><i>%s</i></td><td>%s</td></tr>" $td1 [htmlify $td2]]
                } else {
                    puts -nonewline [format "<tr><td>%s</td><td>%s</td></tr>" [htmlify $td1] [htmlify $td2]]
                }
                puts "</table>\n"
            }
            continue
        }
        if {[regexp {^[Hh]1} $first]} {
            lset fields 0 "#"
            puts $fields
            continue
        }
        if {[regexp {^[Hh]2} $first]} {
            lset fields 0 "##"
            puts $fields
            continue
        }
        if {[regexp {^[Hh]3} $first]} {
            lset fields 0 "###"
            puts $fields
            continue
        }
        if {[regexp {^[Hh]4} $first]} {
            set fields [string map {\"! ! \"@ @ \"| |} $fields]
            lset fields 0 "###"
            puts $fields
            continue
        }
        if {[regexp {^[Hh]5} $first]} {
            lset fields 0 "#####"
            puts $fields
            continue
        }
        if {[regexp {^[Hh]6} $first]} {
            lset fields 0 "######"
            puts $fields
            continue
        }
        # it's for LaTeX, ignore
        if {$first eq "IX"} {
            continue
        }
        if {$first in {IG IF}} {
            puts -nonewline [format "![#](%s)\n" [string range $second 1 end]]
            continue
        }
        if {$first eq "EM"} {
            continue
        }
        if {$first eq "CB("} {
            set in_cb 1
            puts {}
            continue
        }
        if {$first eq "CB)"} {
            set in_cb 0
            continue
        }
        if {$in_cb} {
            puts $line
            continue
        }
        continue
    }
}

flushp
puts "\n"

proc htmlify str {
    string map {& &amp; < &lt; > &gt;} $str
}

# Vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
