from CvDetector import CvDetector
from CvMqtt import CvMqtt
from CvConfig import config
import threading
import json
import sys

mqtt = CvMqtt(
	broker_url=config["mqtt"]["broker_url"], 
	port=config["mqtt"]["port"], 
	debug=config["mqtt"]["debug"]
)

def launch_detector(detector_config):
	print(f"Launching detector for {detector_config['identifier']}")
	detector = CvDetector(
		rtsp_url=detector_config["rtsp_url"],
		handle_object_payload=lambda payload: mqtt.publish(detector_config["identifier"] + "/detection", json.dumps(payload)),
		model_name=detector_config["model_name"],
		processing_frequency=detector_config["processing_frequency"],
		debug=detector_config["debug"]
	)

	detector.main()

def usage():
	print("Usage: python3 CvMain.py <detector_identifier>")
	exit(1)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		usage()

	detector_identifier = sys.argv[1]

	if detector_identifier not in config["detectors"]:
		print(f"Detector {detector_identifier} not found in config")
		usage()

	launch_detector(config["detectors"][detector_identifier])

# launch_detector(config["detectors"]["/carronvale/backyard"])