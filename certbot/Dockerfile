FROM certbot/certbot
COPY . /app
WORKDIR /app
#RUN pip install --upgrade pip \
#&& pip install APScheduler
RUN pip install APScheduler
ENTRYPOINT [ "python", "/app/start.py" ]
#ENTRYPOINT [ "sh" ]
