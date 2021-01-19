import cv2 as cv
import numpy as np

x_point, y_point = -1,-1

def select_points(event, x, y, flags, param):
    global src_x, src_y, drawing
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        src_x, src_y = x, y
        print("coordinate:", src_x, src_y)
        cv.circle(frame, (x, y), 5, (0, 0, 255), -1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False

point_list = []

map = cv.imread('map.png', -1)
cv.namedWindow('map')
cv.moveWindow('map', 80, 80)


# cap = cv.VideoCapture(0) # camera 1개만 부착되어 있기 때문
cap = cv.VideoCapture('video.mov')


while True:
    _, frame = cap.read()

    cv.imshow("Frame", frame)

    print(frame.shape) #404, 720    # 2160, 3840    #1080, 1920

    # 마우스로 점 찍기
    cv.setMouseCallback('frame', select_points)

    # q button 누르면 종료
    if cv.waitKey(1) == ord('q'):
        break
    elif cv.waitKey(1) == ord('s'):
        print('points')
        cv.circle(frame, (x_point, y_point), 5, (0, 255, 0), -1)
        point_list.append([x_point, y_point])
        # print("points:")
        # print(point_list)

    cv.circle(frame, (461, 321), 5, (0, 0, 255), -1)
    cv.circle(frame, (1449, 345), 5, (0, 0, 255), -1)
    cv.circle(frame, (162, 849), 5, (0, 0, 255), -1)
    cv.circle(frame, (1802, 851), 5, (0, 0, 255), -1)

    pts1 = np.float32([[461, 321], [1449, 345], [162, 849], [1802, 851]])
    pts2 = np.float32([[0, 0], [800, 0], [0, 500], [800, 500]])

    # calculates a perspective transform from four pairs of the corresponding points
    matrix = cv.getPerspectiveTransform(pts1, pts2)

    # applies a perspective transformation to an image
    result = cv.warpPerspective(frame, matrix, (800, 500))

    cv.imshow("Perspective transformation", result)


cap.release()
cv.destroyAllWindows()