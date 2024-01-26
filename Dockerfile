FROM python:3.11
RUN apt-get update && apt-get install zsh
RUN PATH="$PATH:/usr/bin/zsh"
WORKDIR /kallabox
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]