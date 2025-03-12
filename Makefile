
P3        = python3
ANSTOTEX  = ./anstotex.py
ANSTOMD   = ./anstomd.py
ANSTOCODE = ./anstocode.py
ANSTOTEST = ./anstotest.py
ANSTOHTML = ./anstohtml.py

.PHONY: all
all: README.md readme.tex readme.html

readme.code: readme.ans
	$(P3) $(ANSTOCODE) $^ >$@

README.md: readme.ans
	$(P3) $(ANSTOMD) $^ >$@

readme.tex: readme.ans
	$(P3) $(ANSTOTEX) $^ >$@

readme.html: readme.ans
	$(P3) $(ANSTOHTML) $^ >$@

.PHONY: clean
clean:
	$(RM) *~

