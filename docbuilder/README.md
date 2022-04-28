## Documentation Builder Docker Image

This docker image will take as input a XXXXX and will XXXX. 

### Building the image

From `internal-docker`, intended to be pushed up to ghcr.io:
```
docker build . -f docbuilder/Dockerfile -t ghcr.io/genapsysinc/docbuilder:latest
```

On a merge to main, this image will be built and pushed up to ghcr.io

### Running the image

The repo to be documented needs to be mounted to /repo on the docker. 

options:
  -h, --help            show this help message and exit
  -c, --confluence      Build and publish to confluence
  -m, --html            Build and publish to html
  -d DIRS [DIRS ...], --dirs DIRS [DIRS ...]
                        Code directories to document
  -w, --warn_as_error   Raise warnings as errors
  -s CONFLUENCE_SECRET, --confluence_secret CONFLUENCE_SECRET
                        Publish to Confluence API token
  -p, --confluence_publish
                        Publish to Confluence

```
docker run -v /path/to/repo/:/repo/ ghcr.io/genapsysinc/docbuilder:latest <options>
```

