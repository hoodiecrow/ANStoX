
foreach file $argv {
    set in_vb 0
    set in_cb 0
    foreachLine line $file {
        set line [regsub {\r} $line {}]
        set fields [split $line]
        set first [lindex $fields 0]
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

# Vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
