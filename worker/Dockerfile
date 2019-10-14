FROM python:3

ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install libc-dev
RUN apt-get -y install build-essential
RUN pip install -U pip

# Install python packages
RUN pip install requests_oauthlib
RUN pip install textblob
RUN pip install gensim
RUN pip install stanfordnlp

# Make directories
RUN mkdir /workdir
RUN mkdir /workdir/worker

# Copy python files
COPY . /workdir/worker
WORKDIR /workdir

ENTRYPOINT ["python3", "-m", "worker.main"]
