ARG BUILD_FROM
FROM $BUILD_FROM

# Esegui con bash come shell predefinita
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Installa dipendenze necessarie
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      git \
      python3 \
      python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Build di libmbus
RUN git clone https://github.com/rscada/libmbus.git /libmbus && \
    cd /libmbus && ./build.sh && make install && ldconfig

# Copia file dell’addon
COPY mbus2mqtt-home-assistant /mbus2mqtt-home-assistant
WORKDIR /mbus2mqtt-home-assistant

# Installa dipendenze Python
RUN pip3 install -r requirements.txt

# Script di avvio
COPY run.sh /
RUN chmod a+x /run.sh

# Avvio gestito da s6-overlay
ENTRYPOINT ["/init"]
