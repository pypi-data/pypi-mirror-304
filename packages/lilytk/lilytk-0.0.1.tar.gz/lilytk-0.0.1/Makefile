.PHONY : help bump-major bump-minor bump-patch clean upload-package upload-test-package 

help : 
	@echo "lilytk - makefile help"
	@echo "----------------------"
	@echo "bump-major          - bump major version"
	@echo "bump-minor          - bump minor version"
	@echo "bump-patch          - bump patch version"
	@echo "clean               - cleans up the build artifacts"
	@echo "install             - install package from source"
	@echo "test                - runs unit tests"
	@echo "upload-package      - builds and uploads the package to PyPi"
	@echo "upload-test-package - builds and uploads the package to Test PyPi"

bump-major :
	bumpver update -n --verbose --major

bump-minor :
	bumpver update -n --verbose --minor

bump-patch :
	bumpver update -n --verbose --patch

clean :
	rm -rf dist

dist/* :
	python3 -m build

install : dist/*
	pip install --force-reinstall dist/lilytk-*.whl

upload-package : dist/*
	twine upload --repository pypi dist/*

upload-test-package : dist/*
	twine upload --repository testpypi dist/*
