python3 = /usr/bin/python3
rm = /bin/rm -fr
pip = /usr/local/bin/pip

test:
	$(python3) -m unittest discover

clean:
	$(rm) __pycache__ \#*\# \.#*

.PHONY: clean test
