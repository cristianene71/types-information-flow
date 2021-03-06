test:
	./run-tests.sh

README.html: README.md
	pandoc -c style.css -f markdown_github < README.md > README.html

%.png: %.dot
	dot $< -Tpng -o $@

%.dot: %.w
	./main.py -g $< -o $@

clean:
		rm -rf parser.out __pycache__ parsetab.py
		rm -f tests/*.dot tests/*.png
