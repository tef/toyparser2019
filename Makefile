all: commonmark json 

commonmark: 
	python3 -m toyparser.commonmark.CommonMark
json: 
	python3 -m toyparser.json.JSON
	python3 -m toyparser.json.test
