FROM python:3.8

COPY item_61.py item_61.py

RUN pip install pandas
RUN pip install pytest
