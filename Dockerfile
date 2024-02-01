FROM python:3.11
WORKDIR /kallabox
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "main.py"]
