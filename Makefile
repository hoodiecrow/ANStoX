
ANSTOTEX  = ./anstotex.awk
ANSTOMD   = ./anstomd.awk
ANSTOCODE = ./anstocode.awk
ANSTOTEST = ./anstotest.awk
ANSTOSCM  = ./anstoscm.awk

.PHONY: all
all: README.md

README.md: readme.ans
	gawk -f $(ANSTOMD) dict.txt $^ >$@

.PHONY: clean
clean:
	$(RM) *~

