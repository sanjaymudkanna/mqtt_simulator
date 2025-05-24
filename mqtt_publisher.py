from pymodbus.client.sync import ModbusTcpClient
import paho.mqtt.client as mqtt
import time
import json

MODBUS_IP = "localhost"
MODBUS_PORT = 5020
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/temperature"

def read_temperature():
    client = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT)
    client.connect()
    rr = client.read_holding_registers(0, 1, unit=1)
    client.close()
    if rr.isError():
        return None
    return rr.registers[0] / 10.0

def publish_temp(mqtt_client):
    while True:
        temp = read_temperature()
        if temp is not None:
            payload = json.dumps({"temperature": temp})
            mqtt_client.publish(MQTT_TOPIC, payload)
            print(f"Published: {payload}")
        else:
            print("Failed to read temperature")
        time.sleep(5)

if __name__ == "__main__":
    mqtt_client = mqtt.Client()
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    publish_temp(mqtt_client)
