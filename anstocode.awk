
{ gsub(/\r/, ""); }

# verbatim block
$1 == "VB(" { in_vb_block = 1 ; next }
$1 == "VB)" { in_vb_block = 0 ; next }
in_vb_block { next }

$1 == "CB("   { in_code_block = 1 ; print "" ; next }
$1 == "CB)"   { in_code_block = 0 ; next }
in_code_block { print }

{ next }

# Vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab:

