import imutils
import cv2
import time
import os
import logging
import itertools
from math import sin, cos, radians
from tracker import EuclideanDistTracker

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")

DATA_DIR = "/data"
MIN_AREA = 500

tracker = EuclideanDistTracker()

base_path = "/usr/local/share/OpenCV/haarcascades/"
face_detector_default = cv2.CascadeClassifier(f"{base_path}/haarcascade_frontalface_default.xml")
face_detector_alt = cv2.CascadeClassifier(f"{base_path}//haarcascade_frontalface_alt.xml")
face_detector_alt2 = cv2.CascadeClassifier(f"{base_path}//haarcascade_frontalface_alt2.xml")
face_detectors = [
    face_detector_default,
    # face_detector_alt,
    # face_detector_alt2
]

def truncate(folder):
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            logger.info(f"deleting: {path}")
            os.remove(path)

def track(tracker, frame):
    _, bbox = tracker.update(frame)
    return bbox

def detect_faces(frame):
    settings = {
        "scaleFactor": None,
        "minNeighbors": None,
        "minSize": (20, 20)
    }
    scales = [1.1, 1.2, 1.3]
    neighbors = [3, 5]

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_faces = []
    for detector in face_detectors:
        for scale in scales:
            for neighbor in neighbors:
                settings["scaleFactor"] = scale
                settings["minNeighbors"] = neighbor
                for angle in [0, -25, 25]:
                    logger.debug(f"detector: {detector.__class__.__name__}, angle: {angle}, scale: {scale}, neighbor: {neighbor}")
                    rimg = rotate_image(frame, angle)
                    faces = detector.detectMultiScale(rimg, **settings)
                    if len(faces):
                        detected_faces = [rotate_point(face, frame, -angle) for face in faces]
    return detected_faces

def draw_info(frame, bboxes):
    if bboxes is not None:
        for bbox in bboxes:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            # Display object ID on frame
            cv2.putText(frame, str(bbox[4]), p1, cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

    # Display FPS on frame
    # timer = cv2.getTickCount()
    # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    # cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

def main(secs=5):
    truncate(DATA_DIR)    
    tracker = EuclideanDistTracker()# cv2.TrackerMIL_create()
    logger.debug("Created MIL tracker")

    start = time.time()
    end = start + secs

    cam = cv2.VideoCapture(0)
    time.sleep(0.5)
    logger.info("Video Capture device initiated")
    # Define an cam bounding box
    # _, frame = video.read()
    

    # Initialize tracker with first frame and bounding box
    # ok = tracker.init(frame, bbox)
    
    # firstFrame = None
    while True:
        _, frame = cam.read()
        # frame = cv2.imread("sample.png")
        logger.info("frame loaded")
        faces = detect_faces(frame)
        logger.info(f"faces detected {len(faces)}")
        face_ids = tracker.update(faces)
        logger.info(f"face ids {len(face_ids)}")
        # box = track(tracker, frame)
        draw_info(frame, face_ids)
        logger.info(f"drawing done")
        frame_time = f"frame_{time.time()}"
        cv2.imwrite(f"/data/{frame_time}.png", frame)
        logger.info(frame_time)
        if time.time() > end:
            break

if __name__ == "__main__":
    main()
