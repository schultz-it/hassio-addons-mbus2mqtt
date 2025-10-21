import hashlib
import json
import os
import paho.mqtt.client as mqtt
import re
import subprocess
import time
import xml.etree.ElementTree as ET
import sys

# Function to generate a unique 8-character hash
def generate_unique_id(name, record_id):
    unique_string = f"{name}_{record_id}"
    hash_object = hashlib.md5(unique_string.encode())
    return hash_object.hexdigest()[:8]

# Function to execute system command and return output
def execute_command(mbus_request_cmd):
    command = mbus_request_cmd.split()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {stderr.decode().strip()}")
        sys.exit(1)
    return stdout.decode()

# Sanitize string to be a valid MQTT topic part
def sanitize_mqtt_topic(topic):
    return re.sub(r'[^a-zA-Z0-9_]', '_', topic)

def parse_and_map_data_record(unit_tag):
    print(f"Parsing and mapping unit_tag: {unit_tag}")
    description = unit = device_class = unit_prefix = None
    scaling_factor = 1.0

    device_class_mapping = {
        'kWh': ('energy', 'k', None),
        'm^3': ('volume', None, 'm³'),
        'W': ('power', None, None),
        'deg C': ('temperature', None, '°C'),
        'm^3/h': ('volume', None, 'm³/h'),
        'd': (None, None, None),
        'time & date': ('timestamp', None, None)
    }

    scaling_factor_mapping = {'m': 0.001, 'k': 1000}

    pattern_full = re.compile(r"([\w\s]+?)\s*\(([\w\.\-]+)\s+([\w\s^/]+)\)")
    pattern_no_factor = re.compile(r"([\w\s]+?)(?=\s*\(|$)\s*(?:\(([^\r\n)]*)\))?")

    match_full = pattern_full.match(unit_tag)
    match_no_factor = pattern_no_factor.match(unit_tag)

    if match_full:
        print(f" -> pattern_full matching")
        description, factor_str, unit = match_full.groups()
        print(f"  -> Factor_str: {factor_str}")
        scaling_factor = scaling_factor_mapping.get(factor_str, 1.0)
        if factor_str:
            try:
                scaling_factor *= float(factor_str)
            except ValueError:
                pass
        print(f"  -> scaling_factor: {scaling_factor}")
    elif match_no_factor:
        print(f" -> pattern_no_factor matching")
        description, unit = match_no_factor.groups()
    else:
        description = unit_tag

    unit = unit.strip() if unit else unit

    if unit in device_class_mapping:
        device_class, unit_prefix, unit_mapped = device_class_mapping[unit]
        unit = unit_mapped if unit_mapped is not None else unit

    print(f"  -> Success, mapped to")
    print(f"     description: {description}")
    print(f"     unit: {unit}")
    print(f"     scaling_factor: {scaling_factor}")
    print(f"     device_class: {device_class}")
    print(f"     unit_prefix: {unit_prefix}")

    return description, unit, scaling_factor, device_class, unit_prefix


# Retrieve and validate environment variables
mqtt_host = os.getenv('MQTT_HOST')
device_name = os.getenv('DEVICE_NAME')
mbus_request_cmd = os.getenv('MBUS_REQUEST_CMD')
mqtt_user = os.getenv('MQTT_USER')
mqtt_password = os.getenv('MQTT_PASSWORD')

if not mqtt_host or not device_name or not mbus_request_cmd:
    print("MQTT_HOST, DEVICE_NAME and MBUS_REQUEST_CMD environment variables are required.")
    sys.exit(1)

try:
    mqtt_host, mqtt_port = mqtt_host.split(':')
    mqtt_port = int(mqtt_port)
except ValueError:
    print("MQTT_HOST environment variable should be in format <fqdn/ipaddress>:<port>.")
    sys.exit(1)

# MQTT client setup with user/password
client = mqtt.Client()
if mqtt_user and mqtt_password:
    client.username_pw_set(mqtt_user, mqtt_password)

print(f"Connecting to MQTT at {mqtt_host}:{mqtt_port} with user {mqtt_user}")
rc = client.connect(mqtt_host, mqtt_port, 60)
print(f"MQTT connect result: {rc}")
if rc != 0:
    print(f"MQTT connection failed with code {rc}. Check credentials or network.")
client.loop_start()


# Main function
def process_xml(publish_discovery):
    xml_data = execute_command(mbus_request_cmd)
    root = ET.fromstring(xml_data)

    slave_info = root.find('.//SlaveInformation')
    manufacturer = slave_info.find('Manufacturer').text if slave_info is not None else "Unknown"
    product_name = slave_info.find('ProductName').text if slave_info is not None else "Unknown"

    for data_record in root.findall('.//DataRecord'):
        record_id = int(data_record.get('id').strip())
        unit_element = data_record.find('Unit')
        scaling_factor = 1.0

        if unit_element is not None and unit_element.text:
            unit_tag = unit_element.text
            description, unit, scaling_factor, device_class, unit_prefix = parse_and_map_data_record(unit_tag)

            value_element = data_record.find('Value')
            if value_element is not None and value_element.text:
                try:
                    value = float(value_element.text)
                    if scaling_factor != 1.0:
                        value *= scaling_factor
                        value = round(value, 1)
                    elif value.is_integer():
                        value = int(value)
                except ValueError:
                    value = value_element.text

                sensor_name = sanitize_mqtt_topic(f"{description}_{record_id}")
                sensor_unique_id = f"{device_name}_{generate_unique_id(sensor_name, record_id)}"

                if publish_discovery:
                    discovery_topic = f"homeassistant/sensor/{device_name}/{sensor_unique_id}/config"
                    discovery_payload = {
                        "name": sensor_name,
                        "uniq_id": sensor_unique_id,
                        "state_topic": f"mbus/{device_name}/{sensor_name}",
                        "value_template": "{{ value_json.value }}",
                        #"device_class": device_class,
                        #"unit_prefix ": unit_prefix,
                        #"unit_of_measurement": unit,
                        "device": {
                            "identifiers": [generate_unique_id(device_name, 0)],
                            "name": device_name,
                            "manufacturer": manufacturer,
                            #"model": product_name,
                        }
                    }

                # Aggiungi unit_of_measurement SOLO se necessario
               # if device_class = "null" and unit:
                  #  discovery_payload["unit_of_measurement"] = unit
# Pubblica su MQTT
                    result = client.publish(discovery_topic, json.dumps(discovery_payload), qos=1, retain=True)
                    print(f"Published discovery: {discovery_topic}, result: {result.rc}")

                print(f"     value: {value}")
                state_topic = f"mbus/{device_name}/{sensor_name}"
                state_payload = {"value": value}
                result2 = client.publish(state_topic, json.dumps(state_payload), qos=1, retain=True)
                print(f"Published state: {state_topic}, result: {result2.rc}")


# Publish discovery messages once
process_xml(publish_discovery=True)

# Repeat polling
while True:
    time.sleep(60)
    process_xml(publish_discovery=False)

client.loop_stop()
client.disconnect()
