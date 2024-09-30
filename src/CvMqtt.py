import paho.mqtt.client as mqtt
class CvMqtt:
	def __init__(self, broker_url, port, debug=False):
		self.broker_url = broker_url
		self.port = port
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_disconnect = self.on_disconnect
		self.connect()
		self.debug = debug

	def on_connect(self, client, userdata, flags, rc):
		print(f"Connected to MQTT broker with result code {rc}")

	def on_disconnect(self, client, userdata, rc):
		print(f"Disconnected from MQTT broker with result code {rc}")
		self.connect()

	def connect(self):
		self.client.connect(self.broker_url, self.port)
		self.client.loop_start()

	def disconnect(self):
		self.client.disconnect()
		self.client.loop_stop()

	def publish(self, topic, payload):
		if self.client.is_connected():
			self.client.publish(topic, payload)
			if self.debug:
				print(f"Publishing to topic {topic}: {payload}")