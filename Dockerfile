FROM python:3.9-slim-buster

COPY FundosCVM.py /
COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

ENTRYPOINT ["python", "/FundosCVM.py"]