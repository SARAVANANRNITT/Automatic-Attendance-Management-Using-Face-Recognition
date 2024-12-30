import requests
import cv2
import numpy as np

url = "" # Put your IP address of your phone camera in here, if it is available.

while True:
    try:
        cam = requests.get(url, timeout=5) # added timeout to avoid request hanging for too long
        imgNp = np.array(bytearray(cam.content), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        cv2.imshow("cam", img)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to camera: {e}") # Handling error if something goes wrong with URL access, and logging the error
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows() # release all resources if the video is closed by hitting "q"