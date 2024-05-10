FROM python:3.9-slim

COPY . /app
WORKDIR /app

RUN pip install -U pip
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]

CMD ["Home.py"]