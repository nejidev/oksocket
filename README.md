ok socket

# simple socket tools
## http_simple.py

# detector host tools
## detector-host.py

	python3
	pip install urllib3

	example:
	1, pre config ip parse file
	curl https://api.github.com/meta -o githubip.txt
	2, add detector 
	https_detector("https://github.com", "githubip.txt")
	3, run adminirstor or root python3 detector-host.py