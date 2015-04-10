"""
::

  Verify whether an image contains a face

  Usage:
    verifier.py <image_path> [--min_area=<min_area>]

  Options:
    -h, --help             Show this screen
    <image_path>           Filepath to image (.jpg, .jpeg, .png)
    --min_area=<min_area>  Minimum rectangular face area [default: 0]
    --version              Show version
"""

import cv2
from docopt import docopt

face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')
lefteye_cascade = cv2.CascadeClassifier('data/haarcascade_mcs_lefteye.xml')
righteye_cascade = cv2.CascadeClassifier('data/haarcascade_mcs_righteye.xml')

def enum(**enums):
  return type('Enum', (), enums)

DETECTOR_CODES = enum(
  ok='Good. Face detected',
  no_face='No face detected',
  not_frontal='Not a frontal face',
  no_eyes='Both eyes not detected',
  too_small='Face too small'
)

def largest_area_index(arr):
  largest_area = 0
  largest_index = 0

  for i, (x, y, w, h) in enumerate(arr):
    area = w * h

    if area > largest_area:
      largest_area = area
      largest_index = i

  return largest_index

def detect_face(img, min_area=0, border_percent=0.1):
  rows, cols = img.shape[:2]
  topborder = int(border_percent * rows)
  leftborder = int(border_percent * cols)
  img = cv2.copyMakeBorder(
    img, topborder, topborder, leftborder, leftborder,
    cv2.BORDER_REPLICATE, value=(0, 0, 0))

  faces = face_cascade.detectMultiScale(img)
  if len(faces) == 0:
    return DETECTOR_CODES.no_face

  index = largest_area_index(faces)
  (x, y, w, h) = faces[index]

  if w * h < min_area:
    return DETECTOR_CODES.too_small

  face_roi = img[y:y+h, x:x+w]
  left_eye = lefteye_cascade.detectMultiScale(face_roi, 2)
  right_eye = lefteye_cascade.detectMultiScale(face_roi, 2)

  if len(left_eye) == 0 or len(right_eye) == 0:
    return DETECTOR_CODES.no_eyes

  return DETECTOR_CODES.ok

def process_img(path, min_area=0):
  img = cv2.imread(path)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  return detect_face(gray, min_area)

if __name__ == "__main__":
  args = docopt(__doc__, version='Face Verifier 1.0')

  print process_img(args['<image_path>'], int(args['--min_area']))
