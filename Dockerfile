From alpine:latest

RUN apk --update add git make python g++ py-pip python-dev && \
    rm -rf /var/cache/apk/*

WORKDIR /root
RUN git clone https://github.com/taku910/mecab.git
RUN cd mecab/mecab && \
    ./configure --with-charset=utf8 && \
    make && \
    make install ; exit 0 && \
    ldconfig
RUN cd mecab/mecab-ipadic && \
    ./configure --with-charset=utf8 && \
    make && \
    make install
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 3001
COPY server.py .
CMD ["python","server.py"]