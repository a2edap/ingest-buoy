FROM tsdat/tsdat:0.2.10

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install -r requirements-dev.txt

WORKDIR /home/root/ingest