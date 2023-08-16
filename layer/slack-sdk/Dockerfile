FROM python:3.7

WORKDIR /work

CMD apt-get update && apt-get install -y zip && apt-get clean && \
    pip install --upgrade pip && \
    pip install slack-sdk -t /python/lib/python3.7/site-packages && \
    zip -r slack-sdk.zip /python/lib/python3.7/site-packages