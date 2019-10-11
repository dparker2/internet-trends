FROM python:alpine

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install gunicorn
RUN pip install falcon
RUN pip install Jinja2

RUN mkdir /workdir
RUN mkdir /workdir/app
RUN mkdir /workdir/test

# Copy start script
COPY ./start.sh /workdir
RUN chmod +x /workdir/start.sh

# Copy python files
COPY ./app /workdir/app
COPY ./test /workdir/test
WORKDIR /workdir

CMD ["./start.sh"]
