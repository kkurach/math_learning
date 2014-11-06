PARTS=computation.tex 

all: clean ssup.pdf computation.pdf

ssup.pdf: 
	pdflatex -shell-escape ssup.tex

computation.pdf: $(PARTS) bibliography.bib ssup.pdf
	pdflatex -shell-escape computation.tex
	bibtex computation
	pdflatex -shell-escape computation.tex
	pdflatex -shell-escape computation.tex
	pdflatex -shell-escape computation.tex

arxiv:
	mkdir arxiv
	cp 00README.XXX arxiv
	cp bibliography.bib arxiv
	cp computation.bbl arxiv
	cp ssup.pdf arxiv
	cp -R figs arxiv
	cp ieee.bst arxiv
	cp nips14submit_e.sty arxiv
	cp computation.tex arxiv 
	cp mcode.sty arxiv

clean:
	rm -f computation.log computation.blg computation.aux computation.pdf computation.4tc computation.xref computation.tmp computation.dvi computation.bbl computation.toc computation.out
	rm -f ssup.log ssup.blg ssup.aux ssup.bbl ssup.4tc ssup.xref ssup.tmp ssup.dvi ssup.bbl ssup.toc ssup.out
	rm -rf arxiv
	rm -rf ~*
	rm -rf *.tmp
	rm -rf *.4om
	rm -rf *~
