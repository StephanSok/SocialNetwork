FROM python:3.10

WORKDIR /app

COPY . .


RUN make install

EXPOSE 8000

CMD ["make", "run-prod"]