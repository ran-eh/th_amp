FROM jupyter/minimal-notebook
USER root
RUN apt-get update && apt-get install -y postgresql
USER 1000
WORKDIR /jupyter
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
# RUN ipynb-py-convert dash.py dash.ipynb
