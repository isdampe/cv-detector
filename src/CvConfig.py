import json

with open("config.json", "r") as f:
	config = json.load(f)

if not config:
	raise Exception("config.json not found")

if not config["mqtt"]:
	raise Exception("mqtt not found in config.json")

if not config["detectors"]:
	raise Exception("detectors not found in config.json")

if not config["mqtt"]["broker_url"]:
	raise Exception("broker_url not found in config.json")

if not config["mqtt"]["port"]:
	raise Exception("port not found in config.json")

if "debug" not in config["mqtt"]:
	raise Exception("debug not found in config.json")

# ensure detectors is a dictionary
if not isinstance(config["detectors"], dict):
	raise Exception("detectors is not a dictionary")

# ensure each detector has the required keys
required_keys = ["rtsp_url", "model_name", "processing_frequency", "identifier"]
for key, detector in config["detectors"].items():
	for key in required_keys:
		if key not in detector:
			raise Exception(f"Missing keys in detector: {key}")