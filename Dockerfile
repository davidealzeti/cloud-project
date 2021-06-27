FROM python:3.8-buster

ENV GET_FILE_FROM_GITHUB = False
ENV SAVE_FILE = False
ENV FILE_FORMAT = json
ENV SELECTED_ANALYSIS = 0

RUN mkdir -p home/saved_files
RUN mkdir -p home/data

COPY data/consegne-vaccini-latest.csv home/data
COPY Analyzer.py /home
COPY requirements.txt /home
COPY start_app.py /home

WORKDIR /home

RUN pip install -r requirements.txt

CMD python start_app.py
