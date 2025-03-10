
foreach file $argv {
    set in_vb 0
    set in_cb 0
    foreachLine line $file {
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
        if {$first eq "TT("} {
            set in_tt 1
            puts {}
            continue
        }
        if {$first eq "TT)"} {
            set in_tt 0
            continue
        }
        if {$in_tt} {
            puts $line
            continue
        }
        continue
    }
}

# Vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
