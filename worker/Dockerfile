FROM python:alpine

ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install requests_oauthlib
RUN pip install textblob

# Make directories
RUN mkdir /workdir
RUN mkdir /workdir/worker

# Copy python files
COPY . /workdir/worker
WORKDIR /workdir

ENTRYPOINT ["python3", "-m", "worker.main"]
