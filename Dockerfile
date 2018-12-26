FROM python:3.7-alpine

RUN apk update \
    && apk upgrade \
    && rm -rf /var/cache/apk/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
ADD app.py /app/
ADD todo /app/todo
WORKDIR /app
EXPOSE 5000
CMD ["python3", "app.py"]
