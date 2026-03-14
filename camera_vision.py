"""
STARK Camera Vision - Live Camera with Auto Detection
NO BUTTON PRESSES - Fully automatic live monitoring
"""

import threading
import time
from typing import Dict, List

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("[Camera] opencv-python not installed. Run: pip install opencv-python")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except Exception:
    DEEPFACE_AVAILABLE = False

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except Exception:
    YOLO_AVAILABLE = False

import config


class CameraVision:
    """Live camera vision system for STARK - No button presses needed"""

    def __init__(self):
        self.camera = None
        self.is_running = False
        self._lock = threading.Lock()
        self.current_frame = None

        self.detected_objects = []
        self.detected_emotion = "neutral"
        self.detected_faces = 0
        self.face_locations = []

        self.analysis_interval = config.CAMERA_ANALYSIS_INTERVAL
        self.last_analysis_time = 0
        self.analysis_result = ""
        self.show_window = False

        self.on_emotion_change = None
        self.on_person_detected = None
        self.on_object_detected = None

        self.emotion_history = []
        self.stable_emotion = "neutral"

        self.yolo_model = None
        self.face_cascade = None

        self._load_models()
        print("[Camera] Vision system initialized.")

    def _load_models(self):
        if not CV2_AVAILABLE:
            return

        if YOLO_AVAILABLE:
            try:
                self.yolo_model = YOLO('yolov8n.pt')
                print("[Camera] YOLO model loaded.")
            except Exception as e:
                print(f"[Camera] YOLO load error: {e}")

        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            print("[Camera] Face detection loaded.")
        except Exception as e:
            print(f"[Camera] Face cascade error: {e}")

    def start_camera(self, show_window: bool = False):
        if not CV2_AVAILABLE:
            print("[Camera] Cannot start — opencv not installed.")
            return
        if self.is_running:
            return

        self.show_window = show_window
        self.is_running = True

        threading.Thread(target=self._camera_loop, daemon=True).start()
        threading.Thread(target=self._analysis_loop, daemon=True).start()

        print("[Camera] Started live monitoring.")

    def _camera_loop(self):
        try:
            self.camera = cv2.VideoCapture(config.CAMERA_INDEX)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

            if not self.camera.isOpened():
                print("[Camera] Cannot open camera.")
                self.is_running = False
                return

            while self.is_running:
                ret, frame = self.camera.read()
                if ret:
                    frame_copy = frame.copy()
                    with self._lock:
                        self.current_frame = frame_copy

                    if self.show_window:
                        self._display_frame(frame)
                        cv2.waitKey(1)

                time.sleep(0.033)

            if self.camera:
                self.camera.release()
            if CV2_AVAILABLE:
                cv2.destroyAllWindows()

        except Exception as e:
            print(f"[Camera] Error: {e}")
            self.is_running = False

    def _display_frame(self, frame):
        display = frame.copy()

        with self._lock:
            face_locs = list(self.face_locations)
            stable_emotion = self.stable_emotion
            detected_faces = self.detected_faces
            detected_objects = list(self.detected_objects)

        for (x, y, w, h) in face_locs:
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(display, "STARK VISION - LIVE", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display, f"Emotion: {stable_emotion}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(display, f"Faces: {detected_faces}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        if detected_objects:
            obj_text = f"Objects: {', '.join(set(o['name'] for o in detected_objects[:3]))}"
            cv2.putText(display, obj_text, (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 0), 1)

        cv2.imshow("STARK Vision", display)

    def _analysis_loop(self):
        while self.is_running:
            try:
                current_time = time.time()
                if (current_time - self.last_analysis_time >= self.analysis_interval
                        and self.current_frame is not None):

                    with self._lock:
                        frame = self.current_frame.copy()
                    self._detect_faces(frame)
                    self._detect_emotions(frame)
                    self._detect_objects(frame)
                    self._build_analysis()
                    self.last_analysis_time = current_time

                time.sleep(0.5)

            except Exception as e:
                print(f"[Camera] Analysis error: {e}")
                time.sleep(1)

    def _detect_faces(self, frame):
        if not CV2_AVAILABLE or self.face_cascade is None:
            return
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            with self._lock:
                self.face_locations = list(faces)
                self.detected_faces = len(faces)
            if len(faces) > 0 and self.on_person_detected:
                self.on_person_detected(len(faces))
        except Exception as e:
            print(f"[Camera] Face detection error: {e}")

    def _detect_emotions(self, frame):
        with self._lock:
            previous_emotion = self.stable_emotion
            current_faces = self.detected_faces
        try:
            if DEEPFACE_AVAILABLE and current_faces > 0:
                results = DeepFace.analyze(
                    frame,
                    actions=['emotion'],
                    enforce_detection=False,
                    silent=True
                )
                if isinstance(results, list) and results:
                    detected_emotion = results[0].get('dominant_emotion', 'neutral')
                elif isinstance(results, dict):
                    detected_emotion = results.get('dominant_emotion', 'neutral')
                else:
                    detected_emotion = 'neutral'

                with self._lock:
                    self.detected_emotion = detected_emotion
                    self.emotion_history.append(detected_emotion)
                    if len(self.emotion_history) > 5:
                        self.emotion_history.pop(0)
                    if len(self.emotion_history) >= 3:
                        if len(set(self.emotion_history[-3:])) == 1:
                            self.stable_emotion = detected_emotion
                    new_stable = self.stable_emotion

                if new_stable != previous_emotion and self.on_emotion_change:
                    self.on_emotion_change(new_stable)
        except Exception as e:
            print(f"[Camera] Emotion detection error: {e}")

    def _detect_objects(self, frame):
        new_objects = []
        try:
            if self.yolo_model and NUMPY_AVAILABLE:
                results = self.yolo_model(frame, verbose=False)
                for r in results:
                    for box in r.boxes:
                        cls = int(box.cls[0])
                        name = self.yolo_model.names[cls]
                        conf = float(box.conf[0])
                        if conf > 0.5:
                            new_objects.append({
                                'name': name,
                                'confidence': round(conf, 2)
                            })
                if new_objects and self.on_object_detected:
                    unique_objects = list(set(o['name'] for o in new_objects))
                    self.on_object_detected(unique_objects)
        except Exception as e:
            print(f"[Camera] Object detection error: {e}")
        with self._lock:
            self.detected_objects = new_objects

    def _build_analysis(self):
        with self._lock:
            detected_faces = self.detected_faces
            stable_emotion = self.stable_emotion
            detected_objects = list(self.detected_objects)
        parts = []
        if detected_faces > 0:
            parts.append(f"I can see {detected_faces} person")
            if stable_emotion and stable_emotion not in ['unknown', '']:
                parts.append(f"appearing {stable_emotion}")
        if detected_objects:
            unique = list(set(obj['name'] for obj in detected_objects))
            if unique:
                parts.append(f"I notice: {', '.join(unique[:5])}")
        with self._lock:
            self.analysis_result = ". ".join(parts) + "." if parts else ""

    def get_current_analysis(self) -> Dict:
        with self._lock:
            return {
                'emotion': self.stable_emotion,
                'faces': self.detected_faces,
                'objects': list(self.detected_objects),
                'summary': self.analysis_result,
                'timestamp': time.time()
            }

    def describe_what_you_see(self) -> str:
        """Get a description — ALWAYS returns something useful"""
        with self._lock:
            analysis_result = self.analysis_result
            detected_faces = self.detected_faces
            stable_emotion = self.stable_emotion
            detected_objects = list(self.detected_objects)
            current_frame = self.current_frame

        if analysis_result:
            return f"Sir, {analysis_result}"

        parts = []
        if detected_faces > 0:
            parts.append(f"I can see {detected_faces} person")
            if stable_emotion not in ['unknown', '']:
                parts.append(f"who appears {stable_emotion}")
        if detected_objects:
            obj_names = list(set(o['name'] for o in detected_objects))
            parts.append(f"I also see: {', '.join(obj_names[:5])}")

        if parts:
            return "Sir, " + ". ".join(parts) + "."

        if not CV2_AVAILABLE:
            return "Sir, camera library is not installed. Please run: pip install opencv-python"

        if current_frame is None:
            return "Sir, camera is starting up. Please wait a moment."

        return "Sir, I can see through the camera. No faces or objects detected clearly right now."

    def get_emotion(self) -> str:
        with self._lock:
            return self.stable_emotion

    def get_objects(self) -> List[Dict]:
        with self._lock:
            return list(self.detected_objects)

    def is_person_present(self) -> bool:
        with self._lock:
            return self.detected_faces > 0

    def get_frame(self):
        with self._lock:
            return self.current_frame

    def capture_photo(self, save_path: str = None) -> str:
        with self._lock:
            frame = self.current_frame
        if frame is None:
            return "Sir, no camera frame available."
        if save_path and CV2_AVAILABLE:
            cv2.imwrite(save_path, frame)
            return f"Sir, photo saved to {save_path}"
        return "Sir, photo captured."

    def set_analysis_interval(self, seconds: int):
        self.analysis_interval = max(1, seconds)

    def show_camera_window(self):
        self.show_window = True

    def hide_camera_window(self):
        self.show_window = False
        if CV2_AVAILABLE:
            cv2.destroyAllWindows()

    def stop_camera(self):
        self.is_running = False
        if self.camera:
            try:
                self.camera.release()
            except Exception:
                pass
        if CV2_AVAILABLE:
            cv2.destroyAllWindows()
        print("[Camera] Stopped.")