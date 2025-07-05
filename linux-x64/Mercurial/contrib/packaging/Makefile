$(eval HGROOT := $(shell cd ../..; pwd))

DEBIAN_CODENAMES := \
  stretch \
  buster \
  bullseye

UBUNTU_CODENAMES := \
  xenial \
  bionic \
  cosmic \
  focal

FEDORA_RELEASE := 31

RHEL_RELEASES := \
  7 \
  8 \
  9

# Build a Python for these RHEL (and derivatives) releases.
RHEL_WITH_PYTHON_RELEASES :=
RHEL_WITH_NONVERSIONED_PYTHON :=
RHEL_WITH_36_DOCUTILS := 7

help:
	@echo 'Packaging Make Targets'
	@echo ''
	@echo 'docker-rhel{$(strip $(RHEL_RELEASES))}'
	@echo '   Build an RPM for a specific RHEL/derivative version using Docker.'
	@echo ''
	@echo 'docker-debian-{$(strip $(DEBIAN_CODENAMES))}'
	@echo '   Build Debian packages specific to a Debian distro using Docker.'
	@echo ''
	@echo 'docker-fedora'
	@echo '   Build an RPM for a Fedora $(FEDORA_RELEASE) using Docker.'
	@echo ''
	@echo 'docker-ubuntu-{$(strip $(UBUNTU_CODENAMES))}'
	@echo '   Build Debian package specific to an Ubuntu distro using Docker.'
	@echo ''
	@echo 'docker-ubuntu-{$(strip $(UBUNTU_CODENAMES))}-ppa'
	@echo '   Build a source-only Debian package specific to an Ubuntu distro'
	@echo '   using Docker.'
	@echo ''
	@echo 'linux-wheels'
	@echo '   Build Linux manylinux wheels using Docker.'
	@echo ''
	@echo 'linux-wheels-{x86_64, i686}'
	@echo '   Build Linux manylinux wheels for a specific architecture using Docker'
	@echo ''
	@echo 'deb'
	@echo '   Build a Debian package locally targeting the current system'
	@echo ''
	@echo 'ppa'
	@echo '   Build a Debian source package locally targeting the current system'
	@echo ''
	@echo 'rhel{$(strip $(RHEL_RELEASES))}'
	@echo '   Build an RPM for a specific RHEL/derivative version locally'
	@echo ''
	@echo 'fedora'
	@echo '   Build an RPM for Fedora $(FEDORA_RELEASE) locally'

.PHONY: help

.PHONY: deb
deb:
	./builddeb

.PHONY: ppa
ppa:
	./builddeb --source-only

# Debian targets.
define debian_targets =
.PHONY: docker-debian-$(1)
docker-debian-$(1):
	./dockerdeb debian $(1)

endef

$(foreach codename,$(DEBIAN_CODENAMES),$(eval $(call debian_targets,$(codename))))

# Ubuntu targets.
define ubuntu_targets =
.PHONY: docker-ubuntu-$(1)
docker-ubuntu-$(1):
	./dockerdeb ubuntu $(1)

.PHONY: docker-ubuntu-$(1)-ppa
docker-ubuntu-$(1)-ppa:
	./dockerdeb ubuntu $(1) --source-only

endef

$(foreach codename,$(UBUNTU_CODENAMES),$(eval $(call ubuntu_targets,$(codename))))

# Fedora targets.
.PHONY: fedora
fedora:
	mkdir -p $(HGROOT)/packages/fedora$(FEDORA_RELEASE)
	./buildrpm
	cp $(HGROOT)/contrib/packaging/rpmbuild/RPMS/*/* $(HGROOT)/packages/fedora$(FEDORA_RELEASE)
	cp $(HGROOT)/contrib/packaging/rpmbuild/SRPMS/* $(HGROOT)/packages/fedora$(FEDORA_RELEASE)
	rm -rf $(HGROOT)/rpmbuild

.PHONY: docker-fedora
docker-fedora:
	./dockerrpm fedora$(FEDORA_RELEASE)

# RHEL targets.
define rhel_targets
.PHONY: rhel$(1)
rhel$(1):
	mkdir -p $$(HGROOT)/packages/rhel$(1)
	./buildrpm $$(if $$(filter $(1),$$(RHEL_WITH_PYTHON_RELEASES)),--withpython,$$(if $$(filter $(1),$$(RHEL_WITH_NONVERSIONED_PYTHON)),--python python,))$$(if $$(filter $(1),$$(RHEL_WITH_36_DOCUTILS)), --docutilspackage python36-docutils,)
	cp $$(HGROOT)/contrib/packaging/rpmbuild/RPMS/*/* $$(HGROOT)/packages/rhel$(1)
	cp $$(HGROOT)/contrib/packaging/rpmbuild/SRPMS/* $$(HGROOT)/packages/rhel$(1)

.PHONY: docker-rhel$(1)
docker-rhel$(1):
	./dockerrpm rhel$(1) $$(if $$(filter $(1),$$(RHEL_WITH_PYTHON_RELEASES)),--withpython,$$(if $$(filter $(1),$$(RHEL_WITH_NONVERSIONED_PYTHON)),--python python,))$$(if $$(filter $(1),$$(RHEL_WITH_36_DOCUTILS)), --docutilspackage python36-docutils,)

endef

$(foreach release,$(RHEL_RELEASES),$(eval $(call rhel_targets,$(release))))

.PHONY: linux-wheels
linux-wheels: linux-wheels-x86_64 linux-wheels-i686

.PHONY: linux-wheels-x86_64
linux-wheels-x86_64:
	docker run -e "HGTEST_JOBS=$(shell nproc)" --rm -ti -v `pwd`/../..:/src quay.io/pypa/manylinux1_x86_64 /src/contrib/packaging/build-linux-wheels.sh

.PHONY: linux-wheels-i686
linux-wheels-i686:
	docker run -e "HGTEST_JOBS=$(shell nproc)" --rm -ti -v `pwd`/../..:/src quay.io/pypa/manylinux1_i686 linux32 /src/contrib/packaging/build-linux-wheels.sh
