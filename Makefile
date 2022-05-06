# Commands for locally building/running different docker images in the repo

docbuilder-img:
	docker build . -f docbuilder/Dockerfile -t ghcr.io/genapsysinc/docbuilder:latest

docbuilder-env: docbuilder-img
	docker run -v `pwd`:/repo -it --entrypoint bash ghcr.io/genapsysinc/docbuilder:latest
