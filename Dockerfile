FROM python:3.12-slim-bookworm

WORKDIR /app  

COPY . /app  

RUN pip install -r requirements.txt  

EXPOSE 8080

CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "8080"]