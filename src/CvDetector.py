import cv2
import torch
import time
import warnings

class CvDetector:
	def __init__(self, rtsp_url: str, handle_object_payload, model_name: str = "yolov5s", processing_frequency: float = 0.2, debug: bool = False):
		self.rtsp_url = rtsp_url
		self.processing_delay = 1 / processing_frequency
		self.model_name = model_name
		self.debug = debug
		self.handle_object_payload = handle_object_payload

	def main(self):
		warnings.filterwarnings("ignore", category=FutureWarning)
		self.model = torch.hub.load("ultralytics/yolov5", self.model_name, pretrained=True)
		self.cap = cv2.VideoCapture(self.rtsp_url)
		if not self.cap.isOpened():
			print("Error: Could not open video stream.")
			return

		self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
		last_capture_time = time.time()

		while True:
			ret, frame = self.cap.read()
			if not ret:
				print("Error: Could not read frame.")
				break

			current_time = time.time()
			if current_time - last_capture_time >= self.processing_delay:
				last_capture_time = current_time
				results = self.model(frame)
				frame = self.detect_objects(frame, results)

				if self.debug:
					cv2.imshow(self.rtsp_url, frame)

			if self.debug:
				if cv2.waitKey(1) & 0xFF == ord("q"):
					break

		self.cap.release()
		if self.debug:
			cv2.destroyAllWindows()

	def on_object_detected(self, object_name: str, confidence: float, bounding_box):
		self.handle_object_payload({
			"label": object_name,
			"confidence": float(confidence),
			"bounding_box": bounding_box
		})
		if self.debug:
			print(f"{object_name} detected with confidence {confidence}")
		
	def detect_objects(self, frame, results):
		labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
		n = len(labels)
		x_shape, y_shape = frame.shape[1], frame.shape[0]

		for i in range(n):
			row = cords[i]
			label = results.names[int(labels[i])]
			confidence = row[4]

			self.on_object_detected(label, confidence, {
				"top_left": [float(row[0]), float(row[1])],
				"bottom_right": [float(row[2]), float(row[3])]
			})

			if self.debug:
				x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
				bgr = (0, 255, 0)  # Green for bounding boxes
				cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
				cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
			
		return frame