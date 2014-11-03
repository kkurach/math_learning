PARTS=computation.tex 

all: clean computation.pdf 

computation.pdf: $(PARTS) bibliography.bib 
	pdflatex -shell-escape computation.tex
	bibtex computation
	pdflatex -shell-escape computation.tex
	pdflatex -shell-escape computation.tex
	pdflatex -shell-escape computation.tex


clean:
	rm -f computation.log computation.blg computation.aux computation.bbl computation.pdf computation.4tc computation.xref computation.tmp computation.dvi computation.bbl computation.toc computation.out
	rm -rf ~*
	rm -rf *.tmp
	rm -rf *.4om
	rm -rf *~
