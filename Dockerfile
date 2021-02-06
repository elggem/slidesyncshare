FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=lti-server.py
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--cert=adhoc"]
