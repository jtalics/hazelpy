# syntax=docker/dockerfile:1
# docker run -it --rm --network=hazel_network --name=hazel_server hazel_server
# https://medium.com/techanic/docker-containers-ipc-using-sockets-part-1-2ee90885602c
# https://docs.docker.com/engine/reference/builder/


# base image
FROM python:3.10.4
RUN useradd --create-home --shell /bin/bash user0
USER user0
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#ARG mode="SERVER"
#ARG host="localhost"
#ARG port="1969"

#Labels as key value pair
LABEL author="jtal"

# Any working directory can be chosen as per choice like '/' or '/home' etc
WORKDIR /hazelpy_server

#to COPY the remote files at working directory in container
COPY . .

EXPOSE 1969
# Now the structure looks like this '/hazelpy_client/main.py'
#RUN echo "Build-time: mode is set to ${mode:-}"

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.
#CMD [ "python",  "main.py", "-m ${mode}", "-h ${host}", "-p ${port}" ]
#CMD [ "python",  "main.py", "-m", "${mode:-}", "-h", "${host:-}", "-p", "${port:-}" ]
#RUN "python main.py -m ${mode} -h ${host} -p ${port}"
CMD [ "python", "main.py", "WEBSOCK", "SERVER", "hazel_websock_server", "1969", "Hazel-websocket-server" ]
