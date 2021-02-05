import numpy as np
from function import PixelMapper, save_lonlat_frame, scaling
##############################################################################

'''
pixel : 실제 공간
lonloat : 도면 공간
실제 mapping 되는 곳에 좌표를 입력 @@@.py 사용
오른쪽 위, 왼쪽 위, 왼쪽 아래, 오른쪽 아래 순서
'''

quad_coords = {
    "pixel": np.array([
        [1448, 348],  # Third lampost top right
        [462, 322],  # Corner of white rumble strip top left
        [163, 847],  # Corner of rectangular road marking bottom left
        [1801, 850]  # Corner of dashed line bottom right
    ]),
    "lonlat": np.array([
        [958, 63],  # Third lampost top right
        [118, 63],  # Corner of white rumble strip top left
        [118, 623],  # Corner of rectangular road marking bottom left
        [958, 623]  # Corner of dashed line bottom right
    ])
}

#PixelMapper로 값 전달
pm = PixelMapper(quad_coords["pixel"], quad_coords["lonlat"])

##############변경해야하는 부분#######################
# 좌표값을 받아야함(하나씩)
f = open("results.txt", 'r')
##################################################
frame = 0
point = dict()
while True:
    line = f.readline()

    if not line:
        break

    info = line[:-1].split(" ")

    frame = info[0]

    if info[0] in point:
        line = point.get(info[0])
        line.append(list(map(int, info[1:])))
    else:
        point[info[0]] = [list(map(int, info[1:]))]

f.close()

###########################################################################

height, weight = save_lonlat_frame(point, pm, int(frame), 'map.png', './demo')

###########################################################################
#scaling
file = open('./scalingPoint.txt', 'w')

for i in range(int(frame)):
    for j in point.get(str(i+1)):
        x_scaled, y_scaled = scaling(j[1], j[2], weight, height)
        file.writelines(str(i+1) + ' ' + str(j[0]) +' ' + str(x_scaled) +' '+str(y_scaled) + '\n')

file.close()

#############################################################################