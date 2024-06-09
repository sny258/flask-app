FROM python:3.10-slim 

WORKDIR /flask-app

COPY requirements.txt app.py database.db .
COPY static/ ./static/
COPY templates/ ./templates/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ]
CMD ["app.py" ]


#docker build -t flask-app:latest .
#docker run -d -p 5000:5000 flask-app:latest

#http://<ec2-public-ip>:5000/login
#http://<ec2-public-dns>:5000/login