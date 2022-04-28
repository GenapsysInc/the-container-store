FROM ubuntu:20.04

COPY docbuilder/apt-requirements.txt /tmp/apt-requirements.txt
COPY docbuilder/python-requirements.txt /tmp/python-requirements.txt

RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y `cat /tmp/apt-requirements.txt`

RUN python3.10 -m ensurepip --upgrade
RUN python3.10 -m pip install --upgrade -r /tmp/python-requirements.txt

COPY docbuilder/assets /assets
COPY docbuilder/scripts /scripts/

ENV PYTHONPATH=PYTHONPATH:/scripts/:/repo/

WORKDIR /repo

ENTRYPOINT ["python3.10", "/scripts/build_sphinx_docs.py"]
