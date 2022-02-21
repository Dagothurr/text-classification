FROM tensorflow/tensorflow:2.7.0

COPY requirements.txt /

RUN pip3 install -r requirements.txt

RUN python -m nltk.downloader stopwords

COPY . /app
WORKDIR /app

ENTRYPOINT ["./gunicorn.sh"]