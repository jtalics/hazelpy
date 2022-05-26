# syntax=docker/dockerfile:1
# docker run -it --rm --network=hazel_network --name=hazel_server hazel_server
# https://medium.com/techanic/docker-containers-ipc-using-sockets-part-1-2ee90885602c
# https://docs.docker.com/engine/reference/builder/

FROM python:3.10.4
RUN useradd --create-home --shell /bin/bash user0
USER user0
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /hazelpy_server
COPY . .
EXPOSE 1969
CMD [ "python", "main.py", "RAWSOCK", "SERVER", "hazel_rawsock_server", "1969", "Hazel-raw-socket-server" ]
