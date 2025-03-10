
{ gsub(/\r/, ""); }

# verbatim block
$1 == "VB(" { invbblock = 1 ; next }
$1 == "VB)" { invbblock = 0 ; next }
invbblock { next }

$1 == "CB("   { incodeblock = 1 ; print "" ; next }
$1 == "CB)"   { incodeblock = 0 ; next }
incodeblock { print }

{ next }

# Vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab:

