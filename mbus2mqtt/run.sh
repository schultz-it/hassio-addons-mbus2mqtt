#!/usr/bin/with-contenv bashio

# Read options
export MQTT_HOST=$(bashio::config 'mqtt_host')
export MQTT_USER=$(bashio::config 'mqtt_user')
export MQTT_PASSWORD=$(bashio::config 'mqtt_password')
export POLL_INTERVAL=$(bashio::config 'poll_interval')
export SERIAL_DEVICE=$(bashio::config 'serial_device')
export BAUDRATE=$(bashio::config 'baudrate')

bashio::log.info "Starting M-Bus to MQTT..."
bashio::log.info "MQTT: ${MQTT_HOST}"
bashio::log.info "Serial: ${SERIAL_DEVICE} @ ${BAUDRATE} baud"
bashio::log.info "Poll interval: ${POLL_INTERVAL}s"

cd /mbus2mqtt-home-assistant

# Get device count
DEVICES_COUNT=$(bashio::config 'mbus_devices | length')
bashio::log.info "Configured ${DEVICES_COUNT} M-Bus device(s)"

# Start process for each device
for i in $(seq 0 $((DEVICES_COUNT - 1))); do
    DEVICE_NAME=$(bashio::config "mbus_devices[${i}].device_name")
    ADDRESS=$(bashio::config "mbus_devices[${i}].address")
    
    export DEVICE_NAME="${DEVICE_NAME}"
    export MBUS_REQUEST_CMD="/libmbus/bin/mbus-serial-request-data -b ${BAUDRATE} ${SERIAL_DEVICE} ${ADDRESS}"
    
    bashio::log.info "Starting: ${DEVICE_NAME} (address ${ADDRESS})"
    
    python3 mbus2mqtt-home-assistant.py &
    
    sleep 2
done

bashio::log.info "All devices started"
wait
