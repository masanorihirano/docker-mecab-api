From alpine:latest

RUN apk --update add git make python g++ py-pip python-dev && \
    rm -rf /var/cache/apk/*

WORKDIR /root
RUN git clone https://github.com/taku910/mecab.git && \
    cd mecab/mecab && \
    ./configure --with-charset=utf8 && \
    make && \
    make install && \
    cd ../mecab-ipadic && \
    ./configure --with-charset=utf8 && \
    make && \
    make install && \
    cd ../.. && \
    rm -r mecab
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 3001
COPY server.py .
CMD ["python","server.py"]