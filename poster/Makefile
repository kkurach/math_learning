all: clean
	pdflatex poster;pdflatex poster;bibtex poster;bibtex poster;pdflatex poster;pdflatex poster
	open poster.pdf

clean:
	rm -f poster.log poster.blg poster.aux poster.pdf poster.4tc poster.xref poster.tmp poster.dvi poster.bbl poster.toc poster.out
	rm -f ssup.log ssup.blg ssup.aux ssup.bbl ssup.4tc ssup.xref ssup.tmp ssup.dvi ssup.bbl ssup.toc ssup.out
	rm -rf arxiv
	rm -rf ~*
	rm -rf *.tmp
	rm -rf *.4om
	rm -rf *~

