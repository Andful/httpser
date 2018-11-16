FROM nginx
COPY . /app
WORKDIR /app
RUN apt-get update \
&& apt-get install -y netcat
CMD ./start.sh
