FROM rockylinux/rockylinux:8.4
#FROM centos:7

RUN yum install -y epel-release && yum -y clean all
RUN yum -y groupinstall "Development Tools" && yum -y clean all
RUN yum install openssl-devel libffi-devel bzip2-devel -y

COPY haiku/yum_requirements.txt /tmp/

RUN set -ex; yum install -v -y $(cat /tmp/yum_requirements.txt) --nogpgcheck && yum clean all

RUN alternatives --set python /usr/bin/python3.9
RUN python -m pip install --upgrade pip wheel

## Install 3rd party tools to /usr/bin
COPY haiku/dependencies/ /usr/bin/
RUN echo 'alias picard="java -jar /usr/bin/picard.jar"' >> ~/.bashrc
RUN for each in /usr/bin/install*.sh ; do bash $each ; done

## Install Python3 libraries
# Assumes python3 is installed in the previous step

COPY haiku/python_requirements.txt /tmp/
# Needed for pysam installation
RUN export HTSLIB_CONFIGURE_OPTIONS=--enable-plugins
RUN python -m pip install -r /tmp/python_requirements.txt
RUN echo 'alias jupyter="jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root"' >> ~/.bashrc
RUN echo 'alias pip="pip3"' >> ~/.bashrc

## Install editable Haiku python library

COPY haiku/pyproject.toml haiku/setup.cfg /
COPY haiku/src/ /src/
RUN python -m pip install -e .

## Copy over local scripts
COPY haiku/scripts /code/scripts
RUN chmod -R 777 /code/scripts

ENV PATH=$PATH:"/code/scripts"
ENTRYPOINT bash
