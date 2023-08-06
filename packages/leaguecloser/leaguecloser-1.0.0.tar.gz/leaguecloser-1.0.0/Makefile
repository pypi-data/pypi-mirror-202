run:
	python src/app.py

test:
	pip install -e .
	pytest tests

package_create:
	pip install build
	python -m build

package_upload:
	pip install twine
	python -m twine upload dist/*

build:
	pyinstaller --clean leaguecloser.spec

.PHONY: run test package_create package_upload build
