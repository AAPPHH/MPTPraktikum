import cv2 as cv
import gdown
from ultralytics import YOLO

# Download YOLO Checkpoint from google drive
url = (
    "https://drive.google.com/file/d/1q-CNPubqyz4OQaPsH5nc5eS2Buy-Fkug/view?usp=sharing"
)
output = "yolo11n.pt"
md5 = "md5:261474e91b15f5ef14a63c21ce6c0cbb"
gdown.cached_download(url, output, hash=md5, fuzzy=True)

# Load the image from disk
image = cv.imread("image.png")

# Load the YOLO-Model
model = YOLO("yolo11n.pt")  # pretrained YOLO11n model

# Run inference on the image
results = model([image])

# Iterate over all results (only one in this case)
for result in results:
    # Iterate over all boxes for current result
    for box in result.boxes:
        # Get the name of the detection
        cls_id = box.cls.item()
        cls_name = result.names[cls_id]

        # Get the coordinates
        x1, y1, x2, y2 = box.xyxy.cpu()[0]

        # Draw a nice frame for visual reference
        cv.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
        cv.rectangle(
            image, (int(x1), int(y1 - 16)), (int(x2), int(y1)), (0, 0, 200), -1
        )  # Filled bar on top
        cv.rectangle(
            image, (int(x1), int(y1 - 16)), (int(x2), int(y1)), (0, 0, 255), 2
        )  # Filled bar on top

        # Put the class label on top
        cv.putText(
            image, cls_name, (int(x1 + 4), int(y1 - 4)), 1, 1, (255, 255, 255), 1
        )

# Display the image and wait for user input
cv.imshow("Image", image)
cv.imwrite("result.png", image)
cv.waitKey(0)
