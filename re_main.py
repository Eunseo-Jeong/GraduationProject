import numpy as np
from function import PixelMapper
from function import save_lonlat_frame
from function import save_dict

##############################################################################

'''
pixel : 실제 공간
lonloat : 도면 공간
실제 mapping 되는 곳에 좌표를 입력 @@@.py 사용
오른쪽 위, 왼쪽 위, 왼쪽 아래, 오른쪽 아래 순서
'''

quad_coords0 = {
    "pixel": np.array([
        [1622, 502],  # Third lampost top right
        [1066, 286],  # Corner of white rumble strip top left
        [700, 934],  # Corner of rectangular road marking bottom left
        [1612, 643]  # Corner                                      of dashed line bottom right
    ]),
    "lonlat": np.array([
        [439, 276],  # Third lampost top right
        [113, 58],  # Corner of white rumble strip top left
        [113, 601],  # Corner of rectangular road marking bottom left
        [439, 385]  # Corner of dashed line bottom right
    ])
}

quad_coords1 = {
    "pixel": np.array([
        [672, 326],  # Third lampost top right
        [215, 506],  # Corner of white rumble strip top left
        [261, 650],  # Corner of rectangular road marking bottom left
        [1019, 827]  # Corner of dashed line bottom right
    ]),
    "lonlat": np.array([
        [874, 113],  # Third lampost top right
        [602, 276],  # Corner of white rumble strip top left
        [602, 384],  # Corner of rectangular road marking bottom left
        [874, 547]  # Corner of dashed line bottom right
    ])
}

# PixelMapper로 값 전달

num = 2

for i in range(num):
    ##############변경해야하는 부분#######################
    # 좌표값을 받아야함(하나씩)
    #     pm = PixelMapper(globals()['quad_coords{}'.format(i)]["pixel"], globals()['quad_coords{}'.format(i)]["lonlat"])

    file = open("results" + str(i) + ".txt", 'r')
    globals()['frame{}'.format(i)], globals()['point{}'.format(i)] = save_dict(file)

    # save_lonlat_frame(globals()['point{}'.format(i)], pm, int(globals()['frame{}'.format(i)]), 'maps.png', './demo')
import cv2
from function import getcolor
import os

map = cv2.imread('maps.png', -1)

for i in range(2):
    globals()['BEV_Point{}'.format(i)] = dict()

# 1541
for frames in range(1, int(globals()['frame{}'.format(0)])):  # object ID마다 색깔바꿔서 점찍기
    for i in range(2):
        pm = PixelMapper(globals()['quad_coords{}'.format(i)]["pixel"], globals()['quad_coords{}'.format(i)]["lonlat"])
        if globals()['point{}'.format(i)].get(str(frames)) != None:
            for label in globals()['point{}'.format(i)].get(str(frames)):
                uv = (label[1], label[2])
                lonlat = list(pm.pixel_to_lonlat(uv))
                li = [label[0], int(lonlat[0][0]), int(lonlat[0][1])]
                if frames in globals()['BEV_Point{}'.format(i)]:
                    line = globals()['BEV_Point{}'.format(i)].get(frames)
                    line.append(li)
                else:
                    globals()['BEV_Point{}'.format(i)][frames] = [li]

                color = getcolor(abs(label[0]))
                cv2.circle(map, (int(lonlat[0][0]), int(lonlat[0][1])), 3, color, -1)

        src = os.path.join('./demo', str(frames) + '.jpg')
        cv2.imwrite(src, map)


# heatmap
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.DataFrame(index=range(0, 12), columns=range(0, 19))
df = df.fillna(0)

measure_df = pd.DataFrame()

for frames in range(1, int(globals()['frame{}'.format(0)])):
    if globals()['BEV_Point{}'.format(0)].get(frames) is not None:
        for label in globals()['BEV_Point{}'.format(0)].get(frames):
            measure_df = measure_df.append(pd.DataFrame([[int(label[1]), int(label[2])]], columns=['x', 'y']))

print(measure_df['x'].max())
print(measure_df['x'].min())
print(measure_df['y'].max())
print(measure_df['y'].min())


for frames in range(1, int(globals()['frame{}'.format(0)])):
    for i in range(num):
        if globals()['BEV_Point{}'.format(i)].get(frames) is not None:
            for label in globals()['BEV_Point{}'.format(i)].get(frames):
                if label[2] < 0 or label[1] < 0 or label[1] > 1041 or label[2] > 668 :
                    continue

    #            print(label[1], label[2],round(int(label[1]) / 1000 * 19), round(int(label[2]) / 600 * 12))
                df.loc[round(int(label[2]) / 668 * 11)][round(int(label[1]) / 1041 * 18)] += 1

file.close()

df = df.replace(0, np.nan)
df = df.reset_index(drop=True)

print(df)
sns.heatmap(df, linewidths=0.1, linecolor="black")
plt.show()