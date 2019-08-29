all: commonmark json yaml rson

commonmark: 
	python3 -m toyparser.commonmark.CommonMark
	python3 -m toyparser.commonmark.test
json: 
	python3 -m toyparser.json.JSON
	python3 -m toyparser.json.test
yaml: 
	python3 -m toyparser.yaml.YAML
	python3 -m toyparser.yaml.test
rson: 
	python3 -m toyparser.rson.RSON
	python3 -m toyparser.rson.test
