release:
	rm dist/*
	python setup.py sdist build
	python -m twine upload dist/*