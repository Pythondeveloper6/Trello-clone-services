FROM python:3.12-slim
WORKDIR /app
RUN apt-get update
COPY requirments.txt .
RUN pip install -r requirments.txt
COPY . .
EXPOSE 8000
CMD [ "python","manage.py","runserver","0.0.0.0:8000"]
