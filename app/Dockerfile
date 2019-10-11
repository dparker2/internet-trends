FROM python:alpine

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install gunicorn
RUN pip install falcon
RUN pip install Jinja2

# Make directories
RUN mkdir /workdir
RUN mkdir /workdir/app

# Copy python files
COPY . /workdir/app
WORKDIR /workdir

ENTRYPOINT ["gunicorn", "--reload", "-b 0.0.0.0:8080", "app.main:app"]
