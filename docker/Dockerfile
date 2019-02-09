FROM python:3.7 as BASE
FROM BASE as BUILD

ARG SSH_KEY
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    echo "${SSH_KEY}" > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa && \
    ssh-keyscan github.com >> ~/.ssh/known_hosts

RUN apt-get install git

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

FROM BASE

COPY --from=BUILD /usr/local/lib/python3.7 /usr/local/lib/python3.7
COPY mantatelegram/bot.py /opt/manta-telegram/mantatelegram/
