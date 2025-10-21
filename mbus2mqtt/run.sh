DEVICES_COUNT=$(bashio::config 'mbus_devices | length')
for i in $(seq 0 $((DEVICES_COUNT - 1))); do
    DEVICE_NAME=$(bashio::config "mbus_devices[${i}].device_name")
    # ...
done