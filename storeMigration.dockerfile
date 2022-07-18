FROM python:3

RUN mkdir -p /opt/src/application
WORKDIR /opt/src/application

COPY application/models.py ./models.py
COPY application/config_store.py ./config_store.py
COPY application/migrate_store.py ./migrate_store.py
COPY application/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/application"

ENTRYPOINT ["python", "./migrate_store.py"]
