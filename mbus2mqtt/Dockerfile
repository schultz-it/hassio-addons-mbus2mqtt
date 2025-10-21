# Use Alpine Linux as the base image
FROM alpine:latest

# Install build dependencies
RUN apk update && apk add \
    gcc \
    g++ \
    make \
    autoconf \
    automake \
    libtool \
    git \
    python3 \
    py3-pip

# Clone the libmbus repository
RUN git clone https://github.com/rscada/libmbus.git

# Change to the libmbus directory
WORKDIR /libmbus

# Build libmbus
RUN ./build.sh
RUN make install

# env for mbus2mqtt
COPY mbus2mqtt-home-assistant /mbus2mqtt-home-assistant
WORKDIR /mbus2mqtt-home-assistant
RUN pip3 install -r requirements.txt --break-system-packages

CMD ["python3", "mbus2mqtt-home-assistant.py"]
