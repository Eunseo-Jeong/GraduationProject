# sync

import re
import cv2
import os
import numpy as np
import ffmpeg

cap1 = cv2.VideoCapture('0218_part1.mp4')
# cap2 = cv2.VideoCapture()
cap2 = cv2.VideoCapture('0218_part2.mp4')

if not cap1.isOpened() and cap2.isOpened():
    print("could not open: ")
    exit(0)

print(int(cap2.get(cv2.CAP_PROP_FRAME_COUNT)))

# 프레임 나누기

count = 1
ret = True
while ret is True:
    ret, image = cap2.read()

    if int(cap2.get(cv2.CAP_PROP_POS_FRAMES)) % 5 == 0:
        count += 1
        continue

    if image is not None:
        cv2.imwrite("./images/frame%d.jpg" % count, image)
        # print('Saved frame%d.jpg' % count)

    count += 1

cap1.release()
cap2.release()

# 비디오 합치기
path = './images/'
paths = [os.path.join(path, i) for i in os.listdir(path) if re.search(".jpg$", i)]
pathOut = './0218_part2(24fps).mov'
fps = 24
frame_array = []


store1, store2, store3 = [], [], []
for i in paths:
    if len(i) == 19:
        store1.append(i)
    elif len(i) == 20:
        store2.append(i)
    elif len(i) == 21:
        store3.append(i)


paths = list(np.sort(store1)) + list(np.sort(store2)) + list(np.sort(store3))
for idx, path in enumerate(paths):
    img = cv2.imread(path)
    height, width, layers = img.shape
    size = (width, height)
    frame_array.append(img)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(pathOut, fourcc, fps, size)

for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])
out.release()

cap3 = cv2.VideoCapture('0218_part2(24fps).mov')
print(int(cap3.get(cv2.CAP_PROP_FRAME_COUNT)))
