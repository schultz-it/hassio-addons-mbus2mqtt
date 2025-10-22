ARG BUILD_FROM
FROM $BUILD_FROM

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Installa dipendenze
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      autoconf \
      automake \
      libtool \
      libltdl-dev \
      git \
      python3 \
      python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Build libmbus
RUN git clone https://github.com/rscada/libmbus.git /libmbus && \
    cd /libmbus && ./build.sh && make install && ldconfig

# Copia i file dell'addon
COPY mbus2mqtt-home-assistant /mbus2mqtt-home-assistant
WORKDIR /mbus2mqtt-home-assistant
RUN pip3 install -r requirements.txt

# Copia run.sh e i servizi S6
COPY run.sh /
COPY rootfs/ /

RUN chmod +x /run.sh
RUN chmod +x /etc/services.d/mbus2mqtt/run
RUN chmod +x /etc/services.d/mbus2mqtt/finish

# Lancia il container tramite s6-overlay
ENTRYPOINT ["/init"]
