test:
	./tests/all_tests.py

end2end:
	./tests/end2end_test.py

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	rm -f *.csv 

