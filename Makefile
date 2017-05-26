test:
	./run-tests.sh

README.html: README.md
	pandoc -c style.css -f markdown_github < README.md > README.html

clean:
		rm -rf parser.out __pycache__ parsetab.py


	


