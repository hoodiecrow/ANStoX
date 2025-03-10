BEGIN {
    print "package require tcltest"
    print "source constcl.tcl\n"
}

END {
    print "\n::tcltest::cleanupTests"
}

{ gsub(/\r/, ""); }

# verbatim block
$1 == "VB(" { invbblock = 1 ; next }
$1 == "VB)" { invbblock = 0 ; next }
invbblock { next }

$1 == "TT("   { intestblock = 1 ; print "" ; next }
$1 == "TT)"   { intestblock = 0 ; next }
intestblock { print }

{ next }

# Vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab:

