# update version.py from most recent version found in CHANGELOG.md
all: version

# retrieve utility script
update_version_from_changelog:
	curl -O https://raw.githubusercontent.com/parmentelat/apssh/master/update_version_from_changelog
	chmod +x $@

version: update_version_from_changelog
	update_version_from_changelog

########## for uploading onto pypi
# this assumes you have an entry 'pypi' in your .pypirc
# see pypi documentation on how to create .pypirc

LIBRARY = nbautoeval

VERSION = $(shell python3 -c "from $(LIBRARY).version import __version__; print(__version__)")
VERSIONTAG = $(LIBRARY)-$(VERSION)
GIT-TAG-ALREADY-SET = $(shell git tag | grep '^$(VERSIONTAG)$$')
# to check for uncommitted changes
GIT-CHANGES = $(shell echo $$(git diff HEAD | wc -l))

# run this only once the sources are in on the right tag
pypi:
	@if [ $(GIT-CHANGES) != 0 ]; then echo "You have uncommitted changes - cannot publish"; false; fi
	@if [ -n "$(GIT-TAG-ALREADY-SET)" ] ; then echo "tag $(VERSIONTAG) already set"; false; fi
	@if ! grep -q ' $(VERSION)' CHANGELOG.md ; then echo no mention of $(VERSION) in CHANGELOG.md; false; fi
	@echo "You are about to release $(VERSION) - OK (Ctrl-c if not) ? " ; read _
	git tag $(VERSIONTAG)
	./setup.py sdist upload -r pypi

# it can be convenient to define a test entry, say testpypi, in your .pypirc
# that points at the testpypi public site
# no upload to build.onelab.eu is done in this case 
# try it out with
# pip install -i https://testpypi.python.org/pypi $(LIBRARY)
# dependencies need to be managed manually though
testpypi: 
	./setup.py sdist upload -r testpypi

