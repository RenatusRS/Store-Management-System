FROM python:3

RUN mkdir -p /opt/src/application
WORKDIR /opt/src/application

COPY application/decorater.py ./decorater.py
COPY application/models.py ./models.py
COPY application/config_store.py ./config_store.py
COPY application/warehouse.py ./warehouse.py
COPY application/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/application"

ENTRYPOINT ["python", "./warehouse.py"]
