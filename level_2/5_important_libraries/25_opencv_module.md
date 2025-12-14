# Deep Dive: OpenCV (`cv2`)

OpenCV (Open Source Computer Vision Library) is the standard for image processing. In Python, it is a wrapper around the C++ library, using NumPy arrays for image data.

---

## 1. The BGR Trap

OpenCV reads images in **BGR** (Blue-Green-Red) order by default, whereas `matplotlib`, `PIL`, and web standards use **RGB**.
**Always** convert if displaying with other libraries.

```python
import cv2

img_bgr = cv2.imread('image.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
```

---

## 2. High-Performance Pixel Access

Never use a `for` loop to iterate over pixels in Python. It's too slow.
Use NumPy slicing or OpenCV's optimized functions.

```python
# SLOW
# for y in range(h):
#     for x in range(w):
#         img[y, x] = 0

# FAST (NumPy)
img[:, :] = 0
```

---

## 3. Image Thresholding & Contours

The bread and butter of object detection (without AI).

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Binary Threshold: Pixels > 127 become 255 (White), else 0 (Black)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find outlines
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
```

---

## 4. Video Processing pipeline

Reading frames is IO-bound. Processing is CPU-bound.
For real-time apps, use `threading` to read frames in a separate thread so the processing loop never waits for the camera.

```python
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret: break
    # Process frame...
```
