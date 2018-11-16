FROM nginx
COPY . /app
WORKDIR /app
RUN apt-get update \
&& apt-get install netcat
CMD ./start.sh
