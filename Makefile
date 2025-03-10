
ANSTOTEX  = ./anstotex.awk
ANSTOMD   = ./anstomd.awk
ANSTOCODE = ./anstocode.awk
ANSTOTEST = ./anstotest.awk
ANSTOHTML = ./anstohtml.awk
ANSTOSCM  = ./anstoscm.awk

.PHONY: all
all: README.md readme.tex readme.html

readme.code: readme.ans
	tclsh90.exe anstocode.tcl $^ >$@

README.md: readme.ans
	perl anstomd.pl $^ >$@

#README.md: readme.ans
#	gawk -f $(ANSTOMD) dict.txt $^ >$@

readme.tex: readme.ans
	gawk -f $(ANSTOTEX) dict.txt $^ >$@

readme.html: readme.ans
	gawk -f $(ANSTOHTML) dict.txt $^ >$@

.PHONY: clean
clean:
	$(RM) *~

