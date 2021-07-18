FROM python:3.9.4-slim-buster
RUN mkdir -p /opt/tail-agent
WORKDIR /opt/tail-agent
COPY tail-agent/requirements.txt .
RUN pip install -r requirements.txt
COPY tail-agent/ /opt/tail-agent/
ENTRYPOINT [ "python", "main.py" ]