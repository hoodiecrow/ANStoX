
Py3        = python3
ANSTO_PATH = ./
ANSTOTEX   = $(ANSTO_PATH)anstotex.py
ANSTOMD    = $(ANSTO_PATH)anstomd.py
ANSTOCODE  = $(ANSTO_PATH)anstocode.py
ANSTOTEST  = $(ANSTO_PATH)anstotest.py
ANSTOHTML  = $(ANSTO_PATH)anstohtml.py

.PHONY: all
all: README.md readme.tex readme.html

source_files = readme.ans

readme.code: $(source_files)
	$(Py3) $(ANSTOCODE) $^ >$@

readme.test: $(source_files)
	$(Py3) $(ANSTOTEST) $^ >$@

README.md: $(source_files)
	$(Py3) $(ANSTOMD) $^ >$@

body.tex: $(source_files)
	$(Py3) $(ANSTOTEX) $^ >$@

readme.tex: preamble.tex body.tex end.tex
	cat $^ >$@

readme.html: $(source_files)
	$(Py3) $(ANSTOHTML) $^ >$@

.PHONY: clean
clean:
	$(RM) *~

