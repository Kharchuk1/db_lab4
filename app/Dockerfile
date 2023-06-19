FROM python:3.11-bullseye AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends p7zip-full

RUN wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/9.19.4/flyway-commandline-9.19.4-linux-x64.tar.gz | tar -xvz && ln -s `pwd`/flyway-9.19.4/flyway /usr/local/bin 

RUN mkdir data
RUN cd data && wget https://zno.testportal.com.ua/yearstat/uploads/OpenDataZNO2019.7z \
    && 7z x -y OpenDataZNO2019.7z && rm OpenDataZNO2019.7z \
    && head -n 1000 Odata2019File.csv > TOdata2019File.csv && mv TOdata2019File.csv Odata2019File.csv
RUN cd data && wget https://zno.testportal.com.ua/yearstat/uploads/OpenDataZNO2020.7z \
    && 7z x -y OpenDataZNO2020.7z && rm OpenDataZNO2020.7z \
    && head -n 1000 Odata2020File.csv > TOdata2020File.csv && mv TOdata2020File.csv Odata2020File.csv

ENV DB=postgres
ENV USER=postgres
ENV PASSWORD=postgres
ENV HOST=db
ENV PORT=5432 
  
ENV REDIS_HOST=cache
ENV REDIS_PORT=6379

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# ENV ACTIVE_DB=mongo 
ENV ACTIVE_DB=postgres

RUN chmod u+x ./entry.sh
CMD ["./entry.sh"]
