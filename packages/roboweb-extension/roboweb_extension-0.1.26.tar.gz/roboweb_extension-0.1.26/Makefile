help:
	cat Makefile

bump-version: .FORCE
	awk -F. -v OFS=. '/^version/{ $$3+=1 }1' settings.ini > settings_new.ini && mv settings_new.ini settings.ini
	perl -i -pe 's/^(version = "([0-9]+)\.([0-9]+)\.)([0-9]+)"/$$1.($$4+1)."\""/e' pyproject.toml


pip: bump-version
	(cd ../../frontend && make jupyter)
	rm -rf dist build
	python -m build
	twine upload --repository pypi dist/*

.FORCE:

