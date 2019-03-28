FROM python:3

ADD ddns.py /

ENTRYPOINT ["python", "./ddns.py"]