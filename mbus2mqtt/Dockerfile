ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install build dependencies
RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    make \
    autoconf \
    automake \
    libtool \
    git \
    python3 \
    py3-pip

# Clone and build libmbus
RUN git clone https://github.com/rscada/libmbus.git /libmbus && \
    cd /libmbus && \
    ./build.sh && \
    make install && \
    ldconfig /usr/local/lib || true

# Copy addon files
COPY mbus2mqtt-home-assistant /mbus2mqtt-home-assistant
WORKDIR /mbus2mqtt-home-assistant

# Install Python dependencies
RUN pip3 install -r requirements.txt --break-system-packages

# Copy and set run script
COPY run.sh /
RUN chmod a+x /run.sh

CMD ["/run.sh"]
