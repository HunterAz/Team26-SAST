FROM python:3.11-rc-bullseye

RUN useradd -m meok
USER meok
WORKDIR /home/meok/website

COPY ./requirements.txt /home/meok/requirements.txt

RUN pip install -r /home/meok/requirements.txt
ENTRYPOINT ["python", "-m", "flask", "run"]
