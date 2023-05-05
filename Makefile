# Commands for locally building/running different docker images in the repo

CODEDIRS = haiku/src/haiku

.PHONY: docbuilder-img
docbuilder-img:
	docker build . -f docbuilder/Dockerfile -t ghcr.io/genapsysinc/docbuilder:latest

.PHONY: docbuilder-env
docbuilder-env: docbuilder-img
	docker run -v `pwd`:/repo -it --entrypoint bash ghcr.io/genapsysinc/docbuilder:latest

.PHONY: haiku-img
haiku-img:
	docker build . -f haiku/Dockerfile -t ghcr.io/genapsysinc/haiku:latest

.PHONY: haiku-env
haiku-env: haiku-img
	docker run -v `pwd`:/repo -it --entrypoint bash ghcr.io/genapsysinc/haiku:latest

.PHONY: html
html:
	docker run -v `pwd`:/repo/ ghcr.io/genapsysinc/docbuilder:latest -m -d $(CODEDIRS)
