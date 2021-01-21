import numpy as np
import os
import cv2

quad_coords = {

    "pixel": np.array([
        [1448, 348],  # Third lampost top right
        [462, 322],  # Corner of white rumble strip top left
        [163, 847],  # Corner of rectangular road marking bottom left
        [1801, 850]  # Corner                                      of dashed line bottom right
    ]),
    "lonlat": np.array([
        [958, 63],  # Third lampost top right
        [118, 63],  # Corner of white rumble strip top left
        [118, 623],  # Corner of rectangular road marking bottom left
        [958, 623]  # Corner of dashed line bottom right
    ])
    # "lonlat": np.array([
    #     [6.602018, 52.036769], # Third lampost top right
    #     [6.603227, 52.036181], # Corner of white rumble strip top left
    #     [6.603638, 52.036558], # Corner of rectangular road marking bottom left
    #     [6.603560, 52.036730] # Corner                                      of dashed line bottom right
    # ]),
    # "pixel": np.array([
    #     [1200, 278], # Third lampost top right
    #     [87, 328], # Corner of white rumble strip top left
    #     [36, 583], # Corner of rectangular road marking bottom left
    #     [1205, 698] # Corner of dashed line bottom right
    # ])
}


def getcolor(idx):
    idx = idx * 3
    return (37 * idx) % 255, (17 * idx) % 255, (29 * idx) % 255


class PixelMapper(object):
    """
    Create an object for converting pixels to geographic coordinates,
    using four points with known locations which form a quadrilteral in both planes
    Parameters
    ----------
    pixel_array : (4,2) shape numpy array
        The (x,y) pixel coordinates corresponding to the top left, top right, bottom right, bottom left
        pixels of the known region
    lonlat_array : (4,2) shape numpy array
        The (lon, lat) coordinates corresponding to the top left, top right, bottom right, bottom left
        pixels of the known region
    """

    def __init__(self, pixel_array, lonlat_array):
        assert pixel_array.shape == (4, 2), "Need (4,2) input array"
        assert lonlat_array.shape == (4, 2), "Need (4,2) input array"
        self.M = cv2.getPerspectiveTransform(np.float32(pixel_array), np.float32(lonlat_array))
        self.invM = cv2.getPerspectiveTransform(np.float32(lonlat_array), np.float32(pixel_array))

    def pixel_to_lonlat(self, pixel):
        """
        Convert a set of pixel coordinates to lon-lat coordinates
        Parameters
        ----------
        pixel : (N,2) numpy array or (x,y) tuple
            The (x,y) pixel coordinates to be converted
        Returns
        -------
        (N,2) numpy array
            The corresponding (lon, lat) coordinates
        """
        if type(pixel) != np.ndarray:
            pixel = np.array(pixel).reshape(1, 2)
        assert pixel.shape[1] == 2, "Need (N,2) input array"
        pixel = np.concatenate([pixel, np.ones((pixel.shape[0], 1))], axis=1)
        lonlat = np.dot(self.M, pixel.T)

        return (lonlat[:2, :] / lonlat[2, :]).T

    def lonlat_to_pixel(self, lonlat):
        """
        Convert a set of lon-lat coordinates to pixel coordinates
        Parameters
        ----------
        lonlat : (N,2) numpy array or (x,y) tuple
            The (lon,lat) coordinates to be converted
        Returns
        -------
        (N,2) numpy array
            The corresponding (x, y) pixel coordinates
        """
        if type(lonlat) != np.ndarray:
            lonlat = np.array(lonlat).reshape(1, 2)
        assert lonlat.shape[1] == 2, "Need (N,2) input array"
        lonlat = np.concatenate([lonlat, np.ones((lonlat.shape[0], 1))], axis=1)
        pixel = np.dot(self.invM, lonlat.T)

        return (pixel[:2, :] / pixel[2, :]).T


pm = PixelMapper(quad_coords["pixel"], quad_coords["lonlat"])

f = open("results.txt", 'r')

point = dict()
while True:
    line = f.readline()
    if not line:
        break
    # print(line)
    info = line[:-1].split(" ")

    if info[0] in point:
        line = point.get(info[0])
        line.append(list(map(int, info[1:])))
    else:
        point[info[0]] = [list(map(int, info[1:]))]
    # print(point)

f.close()

###########################################################################

frame = cv2.imread('capture.PNG', -1)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.moveWindow('frame', 80, 80)
# print(frame.shape)

map = cv2.imread('map.png', -1)
cv2.namedWindow('map')
cv2.moveWindow('map', 780, 80)
# print(map.shape)
# print(type(str(1)))

for frames in range(1, 1541):
    for label in point.get(str(frames)):
        uv = (label[1], label[2])
        lonlat = list(pm.pixel_to_lonlat(uv))
        color = getcolor(abs(label[0]))
        cv2.circle(map, (int(lonlat[0][0]), int(lonlat[0][1])), 3, color, -1)

    src = os.path.join('./demo/', str(frames)+'.jpg')
    cv2.imwrite(src, map)